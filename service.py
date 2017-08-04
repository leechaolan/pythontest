import time
import sqlalchemy as sa
from sqlalchemy import func
import httplib2
import urllib
from oslo_serialization import jsonutils
from oslo_log import log
from storage import tables
from storage import utils

LOG = log.getLogger(__name__)

class Service(object):

	def __init__(self, conf):
		self.conf = conf
		self.periodic_interval = conf.periodic_task_interval
		self.timers = []
		if self.conf.periodic_task_interval is None:
			self.periodic_interval = 60*60*24

	def periodic_task(self):
		print('[%s]periodic is called!' % time.ctime())
		threading.Timer(self.periodic_interval, periodic_task).start()

	def start(self):
		pass

class Periodic_Task(object):

	def __init__(self, conf, storage_controller):
		self._conf = conf
		self._storage_controller = storage_controller
		self.pe_list_result = {}
		self.ce_list_result = {}
		self._host_ip_list = []
		self.pe_row_list = []
		self.ce_row_list = []

	def get_agent_ip(self, pe_code):
		sel_field = [tables.Pe.c.id, 
		             tables.Pe.c.host_id,
	                 tables.Host.c.host_ip_address]
		sel = sa.sql.select(sel_field, 
				            tables.Pe.c.pe_code == pe_code).select_from(tables.Pe.join(tables.Host,
									                                                   tables.Host.c.host_id == tables.Pe.c.host_id))
		result = self._storage_controller.run(sel)
		for i in result:
			print i['host_ip_address']
			host_ip = i['host_ip_address']
			return host_ip

	def get_pe_ip(self, pe_code):
		sel_field = [tables.Pe.c.pe_default_port_ip]
		sel = sa.sql.select(sel_field, tables.Pe.c.pe_code == pe_code)
		result = self._storage_controller.run(sel)

		for i in result:
			pe_ip = i['pe_default_port_ip']
			return pe_ip

	def make_ce_delete_payload(self, list_dict):
		pass

	def make_ce_create_payload(self):
		pass

	def to_agent(self, payload, method):
		ip = self.get_agent_ip(payload['pe_code'])
		pe_ip = self.get_pe_ip(payload['pe_code'])
		payload['pe_ip'] = pe_ip
		payload['method'] = method
		url = 'http://' + str(ip) + ':' + '9001' + '/users'
		print url
		resp = utils.make_notify(payload, url)
		return resp['result']

	def list_boss_pe_endpointt(self):
		http = httplib2.Http()
		timestamp = int(time.time())
		body_dict = {'query_id': timestamp, 'node_code': '', 'host_code': '', 'pe_code': ''}
		resp, context = http.request(self._conf.boss_operate_uri,
				               method="POST",
							   headers={'Context-Type': 'application/x-www-form-urlencoded'},
							   body=urllib.urlencode(body_dict))
		self.pe_list_result = context.decode()

	def format_pe_list_result(self):
		# First compare each item count.
		# If count different chanage it refer to result from BOSS
		LOG.debug(u'begin contrast between local db and result from invoke BOSS list endpoint')
		list_result_decode = jsonutils.loads(self.pe_list_result)
		self._list_result_decode = list_result_decode
		#print self._list_result_decode

		node_count = len(self._list_result_decode['data_list'])
		node_list = self._list_result_decode['data_list']

		row_lst = []
		for i in node_list:
			host_count = len(i['host_list'])
			host_list = i['host_list']
			node_code = i['node_code']
			sel = sa.sql.select([func.count()]).select_from(tables.Host)
			result = self._storage_controller.run(sel)
			select_count = int(result.fetchone()[0])
			for j in host_list:
				if 'pe_list' in j:
					pe_list = j['pe_list']
					pe_count = len(j['pe_list'])
					for k in pe_list:
						pe_row_dict = {}
						pe_row_dict['host_code'] = j['host_code']
						if 'host_type' in j:
							pe_row_dict['host_type'] = j['host_type']
						pe_row_dict['host_work_status'] = j['host_work_status']
						if 'host_ip_address' in j:
							pe_row_dict['host_ip_address'] = j['host_ip_address']
							self._host_ip_list.append(j['host_ip_address'])
						pe_row_dict['node_code'] = i['node_code']
						pe_row_dict['node_type'] = i['node_type']
						pe_row_dict['pe_code'] = k['pe_code']
						pe_row_dict['pe_type'] = k['pe_type']
						pe_row_dict['pe_work_status'] = k['pe_work_status']
						pe_row_dict['pe_default_port_ip'] = k['pe_vm_ip']
						pe_row_dict['pe_vlan_port_ip'] = k['pe_sdn_ip']
						pe_row_dict['pe_vpn_server_ip'] = k['pe_access_server_ip']
						pe_row_dict['pe_vpn_ip_range_start'] = k['pe_access_ip_pool_begin_ip']
						pe_row_dict['pe_vpn_ip_range_end'] = k['pe_access_ip_pool_end_ip']
						pe_row_dict['pe_vpn_access_port'] = k['pe_access_port']
						pe_row_dict['virtual_network_number'] = k['virtual_network_number']
						row_lst.append(pe_row_dict)
		print '\n'
		print row_lst
		for i in row_lst:
			md5str = i['node_code'] +                 \
			         i ['host_code'] +                 \
			         i ['host_type'] +                 \
			         i ['host_work_status'] +          \
			         i ['host_ip_address'] +           \
			         i ['pe_code'] +                   \
			         i ['pe_type'] +                   \
			         i ['pe_work_status'] +            \
			         i ['pe_default_port_ip'] +        \
			         i ['pe_vlan_port_ip'] +           \
			         i ['pe_vpn_server_ip'] +          \
			         i ['pe_vpn_ip_range_start'] +     \
			         i ['pe_vpn_ip_range_end'] +       \
			         i ['pe_vpn_access_port'] +        \
					 i ['virtual_network_number']
			md5sum_code = utils.md5sum(md5str)
			i['pe_row_md5sum'] = md5sum_code
		md5str_total = ''
		for i in row_lst:
			md5str_total += i['pe_row_md5sum']
		md5sum_code_total = utils.md5sum(md5str)
		for i in row_lst:
			i['pe_table_md5sum'] = md5sum_code_total

		self.pe_row_list = row_lst		

	def pe_contrast_to_local_db(self):
		select_fields = [tables.Pe_total.c.id,
		                 tables.Pe_total.c.pe_table_md5sum,
		                 tables.Pe_total.c.pe_table_md5sum,
		                 tables.Pe_total.c.host_code,
		                 tables.Pe_total.c.host_type,
		                 tables.Pe_total.c.host_work_status,
		                 tables.Pe_total.c.host_ip_address,
		                 tables.Pe_total.c.node_code,
		                 tables.Pe_total.c.pe_code,
		                 tables.Pe_total.c.pe_type,
		                 tables.Pe_total.c.pe_work_status,
		                 tables.Pe_total.c.pe_default_port_ip,
		                 tables.Pe_total.c.pe_vlan_port_ip,
		                 tables.Pe_total.c.pe_vpn_server_ip,
		                 tables.Pe_total.c.pe_vpn_ip_range_start,
		                 tables.Pe_total.c.pe_vpn_ip_range_end,
		                 tables.Pe_total.c.pe_vpn_access_port,
		                 tables.Pe_total.c.virtual_network_number,
		                ]

		
		sel = sa.sql.select([func.count()]).select_from(tables.Pe_total)
		result = self._storage_controller.run(sel)
		self._selected_pe_count = int(result.fetchone()[0])
		self._listed_pe_count = len(self.pe_row_list)

		sel = sa.sql.select(select_fields)
		result = self._storage_controller.run(sel)
		# just compare the 'table md5sum' value.
		#if it is different that means Pe count is different 
		#here don't need to consider detail operate because Pe already configed before launch
		for i, v in enumerate(result):
			if v['pe_table_md5sum'] == self.pe_row_list[i]['pe_table_md5sum']:
				return True
				
		sel = sa.sql.select(select_fields)
		result = self._storage_controller.run(sel)
		sel_md5_lst = []
		lis_md5_lst = []
		for i in result:
			sel_md5_lst.append(i['pe_row_md5sum'])

		for j in self.pe_row_list:
			lis_md5_lst.append(j['pe_row_md5sum'])
		
		#print sel_md5_lst
		#print lis_md5_lst

		for i in sel_md5_lst:
			if i not in lis_md5_lst:
				sel = sa.sql.select([tables.Pe_total.c.pe_code])
				result = self._storage_controller.run(sel)
				pe_code = result.fetchone()['pe_code']
				de = tables.Pe_total.delete().where(tables.Pe_total.pe_row_md5sum == i)
				self._storage_controller.run(de)
				de = tables.Pe.delete().where(tables.Pe.pe_code == pe_code)
				self._storage_controller.run(de)

		for i in lis_md5_lst:
			if i not in sel_md5_lst:
				for j in self.pe_row_list:
					if j['pe_row_md5sum'] == i:
						print j['host_code']
						sel = sa.sql.select([tables.Host.c.host_id]).where(tables.Host.c.host_code == j['host_code'])
						result = self._storage_controller.run(sel)
						host_id = None
						for i in result:
							host_id = i['host_id']
						print host_id
						ins = sa.sql.expression.insert(tables.Pe).values(host_id=host_id,
												        pe_code =j['pe_code'],
														pe_type=j['pe_type'],
														pe_work_status=j['pe_work_status'],
														pe_default_port_ip=j['pe_default_port_ip'],
														pe_vlan_port_ip=j['pe_vlan_port_ip'],
														pe_vpn_server_ip=j['pe_vpn_server_ip'],
														pe_vpn_ip_range_start=j['pe_vpn_ip_range_start'],
														pe_vpn_ip_range_end=j['pe_vpn_ip_range_end'],
														pe_vpn_access_port=j['pe_vpn_access_port'],
														virtual_network_number=j['virtual_network_number'])
						self._storage_controller.run(ins)
						ins = sa.sql.expression.insert(tables.Pe_total).values(pe_row_md5sum=j['pe_row_md5sum'],
								                              pe_table_md5sum=j['pe_table_md5sum'],
															  host_code=j['host_code'],
															  host_type=j['host_type'],
															  host_work_status=j['host_work_status'],
															  host_ip_address=j['host_ip_address'],
															  node_code=j['node_code'],
															  pe_code=j['pe_code'],
															  pe_type=j['pe_type'],
															  pe_work_status=j['pe_work_status'],
															  pe_default_port_ip=j['pe_default_port_ip'],
															  pe_vlan_port_ip=j['pe_vlan_port_ip'],
															  pe_vpn_server_ip=j['pe_vpn_server_ip'],
															  pe_vpn_ip_range_start=j['pe_vpn_ip_range_start'],
															  pe_vpn_ip_range_end=j['pe_vpn_ip_range_end'],
															  pe_vpn_access_port=j['pe_vpn_access_port'],
															  virtual_network_number=j['virtual_network_number'])
						self._storage_controller.run(ins)
		return False

	def list_boss_ce_endpoint(self):
		http = httplib2.Http()
		timestamp = int(time.time())
		body_dict = {'query_id': timestamp, 'customer_id': '', 'customer_code': '', 'virtual_network_number': ''}
		ce_list_result = utils.make_notify(body_dict, self._conf.boss_business_config_url)
		result_dict = jsonutils.loads(ce_list_result)
		self.ce_list_result = result_dict

	def format_ce_list_result(self):
		#print self.ce_list_result
		access_instance_list =  []
		data_list = self.ce_list_result['data_list']
		for i in data_list:
			vnet_list = i['virtual_network_list']
			for j in vnet_list:
				instance_list = j['access_instance_list']
				for k in instance_list:
					access_instance_dict = {}
					access_instance_dict['virtual_network_number'] = j['virtual_network_number']
					access_instance_dict['customer_id'] = i['customer_id']
					access_instance_dict['customer_code'] = i['customer_code']
					access_instance_dict['access_instance_id'] = k['access_instance_id']
					access_instance_dict['tunnel_type'] = k['tunnel_type']
					access_instance_dict['vpn_cli_ip'] = k['openvpn_client_ip']
					access_instance_dict['username'] = k['username']
					access_instance_dict['password'] = k['password']
					access_instance_dict['work_mode'] = k['work_mode']
					access_instance_dict['pe_code'] = k['pe_code']
					row_md5 = access_instance_dict['virtual_network_number'] +    \
					          str(access_instance_dict['customer_id']) +               \
					          str(access_instance_dict['customer_code']) +             \
					          str(access_instance_dict['access_instance_id']) +        \
					          str(access_instance_dict['tunnel_type']) +               \
					          str(access_instance_dict['vpn_cli_ip']) +                \
					          str(access_instance_dict['username']) +                  \
					          str(access_instance_dict['password']) +\
					          str(access_instance_dict['work_mode']) +\
	                          str(access_instance_dict['pe_code'])
					row_md5_value = utils.md5sum(row_md5)
					access_instance_dict['ce_row_md5sum'] = row_md5_value
					access_instance_list.append(access_instance_dict)
		self.ce_row_list = access_instance_list
		ce_table_md5 = ''
		for i in self.ce_row_list:
			ce_table_md5 += i['ce_row_md5sum']
		ce_table_md5sum = utils.md5sum(ce_table_md5)
		for i in self.ce_row_list:
			i['ce_table_md5sum'] = ce_table_md5sum
		print self.ce_row_list

	def ce_contrast_to_local_db(self):
		select_fields = [tables.Ce_total.c.id,
		                 tables.Ce_total.c.ce_row_md5sum,
		                 tables.Ce_total.c.ce_table_md5sum,
		                 tables.Ce_total.c.virtual_network_number,
		                 tables.Ce_total.c.customer_id,
		                 tables.Ce_total.c.customer_code,
		                 tables.Ce_total.c.access_instance_id,
		                 tables.Ce_total.c.tunnel_type,
		                 tables.Ce_total.c.vpn_cli_ip,
		                 tables.Ce_total.c.username,
		                 tables.Ce_total.c.password,
		                 tables.Ce_total.c.work_mode,
		                 tables.Ce_total.c.pe_code
		                ]
		sel = sa.sql.select([func.count()]).select_from(tables.Ce_total)
		result = self._storage_controller.run(sel)
		self._selected_ce_count = int(result.fetchone()[0])
		self._listed_ce_count = len(self.ce_row_list)

		sel = sa.sql.select(select_fields)
		result = self._storage_controller.run(sel)
		for i, v in enumerate(result):
			if v['ce_table_md5sum'] == self.ce_row_list[i]['ce_table_md5sum']:
				return True

		sel = sa.sql.select(select_fields)
		result = self._storage_controller.run(sel)
		sel_md5_lst = []
		lis_md5_lst = []
		for i in result:
			sel_md5_lst.append(i['ce_row_md5sum'])

		for j in self.ce_row_list:
			lis_md5_lst.append(j['ce_row_md5sum'])
		
		#print sel_md5_lst
		#print lis_md5_lst
		

		for i in sel_md5_lst:
			if i not in lis_md5_lst:
				sel = sa.sql.select([tables.Ce_total.username,
				                     tables.Ce_total.password,
				                     tables.Ce_total.vpn_cli_ip,
				                     tables.Ce_total.pe_code,
				                     tables.Ce_total.ce_row_md5sum], 
									 tables.Ce_total.ce_row_md5sum == i)
				result = self._storage_controller.run(sel)
				for j in result:
					self.to_agent(dict(j), 'delete')
				de = tables.Pe_total.delete().where(tables.Ce_total.ce_row_md5sum == i)
				self._storage_controller.run(de)

		for i in lis_md5_lst:
			if i not in sel_md5_lst:
				for j in self.ce_row_list:
					if j['ce_row_md5sum'] == i:
						self.to_agent(dict(j), 'create')
						sel = sa.sql.select([tables.Pe.id], tables.Pe.pe_code == payload['pe_code'])
						result = self._storage_controller.run(sel)
						for k in result:
							pe_id = k['pe_id']
						ins = sa.sql.expression.insert(tables.Ce).values(virtual_network_number=j['virtual_network_number'],
						#ins = tables.Ce.insert().values(virtual_network_number=j['virtual_network_number'],
							                                             customer_id=j['customer_id'],
																		 customer_cod=j['customer_code'],
																		 access_instance_id=j['access_instance_id'],
																		 tunnel_type=j['tunnel_type'],
																		 vpn_cli_ip=j['vpn_cli_ip'],
																		 username=j['username'],
																		 password=j['password'],
																		 work_mode=j['work_mode'],
																		 pe_id=pe_id)
						self._storage_controller.run(ins)
						ins = sq.sql.expression.insert(tables.Ce_total).values(ce_row_md5sum=j['ce_row_md5sum'],
							                                                   ce_table_md5sum=j['ce_table_md5'],
																			   virtual_network_number=j['virtual_network_number'],
																			   customer_id=j['customer_id'],
																			   customer_code=j['customer_code'],
																			   access_instance_id=j['access_instance_id'],
																			   tunnel_type=j['tunnel_type'],
																			   vpn_cli_ip=j['vpn_cli_ip'],
																			   username=j['username'],
																			   password=j['password'],
																			   work_mode=j['work_mode'],
																			   pe_code=j['pe_code'])

