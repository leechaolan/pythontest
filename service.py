import time
import threading
import socket
import sqlalchemy as sa
from sqlalchemy import func
import httplib2
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

#This do a synchronization task. compare md5 checksum between local database and result from BOSS,
#for each row in table make a md5digest and merge each row md5 again, 
#if the latter both the same so it is syncchronous
class Periodic_Task(object):

	def __init__(self, conf, storage_controller):
		self._conf = conf
		self._storage_controller = storage_controller
		self._pe_list_result = {}
		self._ce_list_result = {}
		self._host_ip_list = []
		self._pe_row_list = []
		self._ce_row_list = []
		self._notify_list_create = []
		self._notify_list_delete = []
		self._node_list = []

	def _get_agent_ip(self, pe_code):
		sel_field = [tables.Host.c.host_ip_address,
		             tables.Pe.c.id,
		             tables.Pe.c.host_id]
		LOG.debug(u'Get pe_code:%(pe_code)s', {'pe_code':pe_code})
		sel = sa.sql.select([tables.Host.c.host_ip_address], 
				            tables.Pe.c.pe_code == pe_code).select_from(tables.Pe.join(tables.Host,
									                                                   tables.Host.c.host_id == tables.Pe.c.host_id))
		result = self._storage_controller.run(sel)
		for i in result:
			iplist = jsonutils.loads(i[0])
			for j in iplist:
				return j['host_ip_address']

	def _get_pe_ip(self, pe_code):
		sel_field = [tables.Pe.c.pe_default_port_ip]
		sel = sa.sql.select(sel_field, tables.Pe.c.pe_code == pe_code)
		result = self._storage_controller.run(sel)

		for i in result:
			pe_ip = i['pe_default_port_ip']
			return pe_ip

	def _get_vlan_port_ip(self, pe_code):
		sel_field = [tables.Pe.c.pe_vlan_port_ip]
		sel = sa.sql.select(sel_field, tables.Pe.c.pe_code == pe_code)
		result = self._storage_controller.run(sel)
		for i in result:
			pe_vlan_port_ip = i['pe_vlan_port_ip']
			return pe_vlan_port_ip

	def looping_call_agent(self, payload, method):
		result = self.to_agent(payload, method)
		default_call_interval = 20
		args = []
		args.append(payload)
		args.append(method)
		t = threading.Timer(default_call_interval, self.looping_call_agent, args)
		t.daemon = True
		t.start()
		if result is 1:
			t.cancel()
			if method is 'create':
				self._notify_list_create.remove(payload['access_instance_id'])
			if method is 'delete':
				self._notify_list_delete.remove(payload['access_instance_id'])
		if self._notify_list_create is [] or self._notify_list_delete is []:
			self.notify_boss()

	def to_agent(self, payload, method):
		print payload
		print method
		ip = self._get_agent_ip(payload['pe_code'])
		pe_ip = self._get_pe_ip(payload['pe_code'])
		payload['pe_ip'] = pe_ip
		payload['method'] = method
		pe_vlan_port_ip = self._get_vlan_port_ip(payload['pe_code'])
		payload['pe_vlan_port_ip'] = pe_vlan_port_ip
		LOG.debug(u'To agent agent_ip: %(agent_ip)s payload:%(payload)s method:%(method)s', 
				  {'agent_ip': ip, 'payload': payload, 'method': method})
		url = 'http://' + str(ip) + ':' + '9001' + '/users'
		resp = utils.make_notify(payload, url)
		print("result: {0}".format(resp))
		LOG.debug(u'Agent response result:%s', resp)
		if resp != {}:
			return resp['result']

		return {}

	def list_boss_pe_endpointt(self):
		http = httplib2.Http()
		http.force_exception_to_status_code = True
		timestamp = int(time.time())
		body_dict = {'query_id': timestamp, 'node_code': '', 'host_code': '', 'pe_code': ''}
		try:
			resp, context = http.request(self._conf.boss_operate_config_url,
					                     method="POST",
			                             body=jsonutils.dumps(body_dict))
		except (httplib2.HttpLib2Error, socket.error) as ex:
			LOG.error(u'POST %s %s', self._conf.boss_operate_config_url, context)
			raise
		if resp.status is 200:
			#print context.decode()
			LOG.debug(u'List BOSS endpoint response status code=%(status_code)d' % 
					  {'status_code': resp.status})
			self._pe_list_result = context.decode()
		else:
			LOG.error(u'POST %s %s', self._conf.boss_operate_config_url, resp.reason)

	def format_pe_list_result(self):
		if self._pe_list_result:
			list_result_decode = jsonutils.loads(self._pe_list_result)
			self._list_result_decode = list_result_decode

			node_count = len(self._list_result_decode['data_list'])
			node_list = self._list_result_decode['data_list']
			self._node_list = node_list
			row_lst = []
			for i in node_list:
				host_count = len(i['host_list'])
				host_list = i['host_list']
				node_code = i['node_code']
				for j in host_list:
					if 'pe_list' in j:
						pe_list = j['pe_list']
						pe_count = len(j['pe_list'])
						for k in pe_list:
							pe_row_dict = {}
							pe_row_dict['host_code'] = j['host_code']
							if 'host_type' in j:
								pe_row_dict['host_type'] = j['host_type']
							if 'host_ip_address_list' in j:
								host_ip_list = []
								host_ip_address_dict = {}
								for p in j['host_ip_address_list']:
									host_ip_address_dict['host_ip_address'] = p['host_ip_address']
									host_ip_address_dict['operator_code'] = p['operator_code']
									host_ip_list.append(host_ip_address_dict)
								#pe_row_dict['host_ip_address_list'] = j['host_ip_address_list']
								pe_row_dict['host_ip_address_list'] = host_ip_list
								#self._host_ip_list.append(j['host_ip_address_list'])
								self._host_ip_list.append(host_ip_list)
							pe_row_dict['node_code'] = i['node_code']
							#pe_row_dict['node_type'] = i['node_type']
							pe_row_dict['pe_code'] = k['pe_code']
							pe_row_dict['pe_type'] = k['pe_type']
							pe_row_dict['pe_vlan_port_ip'] = k['pe_sdn_ip']
							pe_row_dict['pe_default_port_ip'] = k['pe_vm_ip']
							if k['pe_type'] != 'monitor':
								pe_row_dict['pe_vpn_server_ip'] = k['pe_access_server_ip']
								pe_row_dict['pe_vpn_ip_range_start'] = k['pe_access_ip_pool_begin_ip']
								pe_row_dict['pe_vpn_ip_range_end'] = k['pe_access_ip_pool_end_ip']
								pe_row_dict['pe_vpn_access_port'] = k['pe_access_port']
								pe_row_dict['virtual_network_number'] = k['virtual_network_number']
							else:
								pe_row_dict['pe_vpn_server_ip'] = ''
								pe_row_dict['pe_vpn_ip_range_start'] = ''
								pe_row_dict['pe_vpn_ip_range_end'] = ''
								pe_row_dict['pe_vpn_access_port'] = 0
								pe_row_dict['virtual_network_number'] = 0
							row_lst.append(pe_row_dict)
			for i in row_lst:
				if i['pe_type'] != 'monitor':
					md5str = i['node_code'] +                 \
							 i['host_code'] +                 \
							 i['host_type'] +                 \
				         	 i['pe_code'] +                   \
				         	 i['pe_type'] +                   \
				         	 i['pe_default_port_ip'] +        \
				         	 i['pe_vpn_server_ip'] +          \
				         	 i['pe_vpn_ip_range_start'] +     \
				         	 i['pe_vpn_ip_range_end'] +       \
				         	 i['pe_vpn_access_port'] +        \
						 	 i['virtual_network_number']
				else:
					md5str = i['node_code'] +                 \
							 i['host_code'] +                 \
							 i['host_type'] +                 \
				         	 i['pe_code'] +                   \
							 i['pe_type'] +                   \
							 i['pe_default_port_ip']
				for j in i['host_ip_address_list']:
					md5str += j['host_ip_address']
					md5str += j['operator_code']
				md5sum_code = utils.md5sum(md5str)
				i['pe_row_md5sum'] = md5sum_code
			#Merge each row to a long string and do md5 checksum. Prestore it and compare later.
			md5str_total = ''
			for i in row_lst:
				md5str_total += i['pe_row_md5sum']
			md5sum_code_total = utils.md5sum(md5str_total)
			for i in row_lst:
				i['pe_table_md5sum'] = md5sum_code_total
			self._pe_row_list = row_lst

	#Through Compare the md5 checksum between local database and result from BOSS to whether to do synchronization.
	def pe_contrast_to_local_db(self):
		select_fields = [tables.Pe_total.c.id,
		                 tables.Pe_total.c.pe_row_md5sum,
		                 tables.Pe_total.c.pe_table_md5sum,
		                 tables.Pe_total.c.host_code,
		                 tables.Pe_total.c.host_type,
		                 tables.Pe_total.c.host_ip_address,
		                 tables.Pe_total.c.node_code,
		                 tables.Pe_total.c.pe_code,
		                 tables.Pe_total.c.pe_type,
		                 tables.Pe_total.c.pe_default_port_ip,
		                 tables.Pe_total.c.pe_vlan_port_ip,
		                 tables.Pe_total.c.pe_vpn_server_ip,
		                 tables.Pe_total.c.pe_vpn_ip_range_start,
		                 tables.Pe_total.c.pe_vpn_ip_range_end,
		                 tables.Pe_total.c.pe_vpn_access_port,
		                 tables.Pe_total.c.virtual_network_number,]
		sel = sa.sql.select([func.count()]).select_from(tables.Pe_total)
		result = self._storage_controller.run(sel)
		self._selected_pe_count = int(result.fetchone()[0])
		self._listed_pe_count = len(self._pe_row_list)

		sel = sa.sql.select(select_fields)
		result = self._storage_controller.run(sel)
		LOG.debug(u'Sync data between local and get from BOSS')
		LOG.debug(u'from BOSS pe count is %d', self._listed_pe_count)
		LOG.debug(u'from loacal db pe count is %d', self._selected_pe_count)
		if self._selected_pe_count is self._listed_pe_count:
			LOG.debug(u'Same count.')
			for i, v in enumerate(result):
				if v['pe_table_md5sum'] == self._pe_row_list[i]['pe_table_md5sum']:
					LOG.debug(u'Pe total md5hash checksum from local db:%s', v['pe_table_md5sum'])
					LOG.debug(u'Pe total md5hash checksumn from BOSS:%s', self._pe_row_list[i]['pe_table_md5sum'])
					LOG.debug(u'Same result.')
					LOG.debug(u'Pe synchronization finished.')
					return True
	
		LOG.debug(u'Any of invoke results is different from select results. Begin compare each item.')
		sel = sa.sql.select([tables.Node.c.node_id])
		result = self._storage_controller.run(sel)
		if result.rowcount is 0:
			for i in self._node_list:
				host_list_temp = i['host_list']
				for j in host_list_temp:
					ip_list_temp = j.get('host_ip_address_list')
					if ip_list_temp:
						ip_ad_list = []
						for k in ip_list_temp:
							ip_ad_list_dict_temp = {}
							ip_ad_list_dict_temp['operator_code'] = k['operator_code']
							ip_ad_list_dict_temp['host_ip_address'] = k['host_ip_address']
							ip_ad_list.append(ip_ad_list_dict_temp)
				ins = sa.sql.expression.insert(tables.Node).values(node_code=i['node_code'])
				result = self._storage_controller.run(ins)
				_primary_key = result.inserted_primary_key[0]
				if i['host_list']:
					for j in i['host_list']:
						host_ip_list_temp = j.get('host_ip_address_list')
						host_ip_list_temp_json = jsonutils.dumps(host_ip_list_temp)
						if host_ip_list_temp:
							ins = sa.sql.expression.insert(tables.Host).values(node_id=_primary_key,
									                                           host_type=j['host_type'],
																			   host_code=j['host_code'],
																			   host_ip_address=host_ip_list_temp_json)
							self._storage_controller.run(ins)

		sel_md5_lst = []
		lis_md5_lst = []
		if self._listed_pe_count:
			sel = sa.sql.select(select_fields)
			result = self._storage_controller.run(sel)
			for i in result:
				sel_md5_lst.append(i['pe_row_md5sum'])

		for j in self._pe_row_list:
			lis_md5_lst.append(j['pe_row_md5sum'])
		#print sel_md5_lst
		#print lis_md5_lst
		for i in sel_md5_lst:
			if i not in lis_md5_lst:
				sel = sa.sql.select([tables.Pe_total.c.pe_code])
				result = self._storage_controller.run(sel)
				pe_code = result.fetchone()['pe_code']
				de = tables.Pe_total.delete().where(tables.Pe_total.c.pe_row_md5sum == i)
				self._storage_controller.run(de)
				de = tables.Pe.delete().where(tables.Pe.c.pe_code == pe_code)
				self._storage_controller.run(de)
		self._update_pe_total_table_md5sum()

		for i in lis_md5_lst:
			if i not in sel_md5_lst:
				for j in self._pe_row_list:
					if j['pe_row_md5sum'] == i:
						sel = sa.sql.select([tables.Host.c.host_id]).where(tables.Host.c.host_code == j['host_code'])
						result = self._storage_controller.run(sel)
						if result.rowcount:
							for i in result:
								host_id = i['host_id']
								LOG.debug(u'Get host_id=%(host_id)d', {'host_id': host_id})

							pe_access_ser_ip = j.get('pe_vpn_server_ip')
							pe_access_pool_start = j.get('pe_vpn_ip_range_start')
							pe_access_pool_end = j.get('pe_vpn_ip_range_end')
							pe_access_port = j.get('pe_vpn_access_port')
							virt_port_no = j.get('virtual_network_number')

							ins = sa.sql.expression.insert(tables.Pe).values(host_id=host_id,
													        pe_code =j['pe_code'],
															pe_type=j['pe_type'],
															pe_default_port_ip=j['pe_default_port_ip'],
															pe_vlan_port_ip=j['pe_vlan_port_ip'],
															pe_vpn_server_ip=pe_access_ser_ip,
															pe_vpn_ip_range_start=pe_access_pool_start,
															pe_vpn_ip_range_end=pe_access_pool_end,
															pe_vpn_access_port=pe_access_port,
															virtual_network_number=virt_port_no)
							self._storage_controller.run(ins)
							ins = sa.sql.expression.insert(tables.Pe_total).values(pe_row_md5sum=j['pe_row_md5sum'],
									                              pe_table_md5sum=j['pe_table_md5sum'],
																  host_code=j['host_code'],
																  host_type=j['host_type'],
																  host_ip_address=str(j['host_ip_address_list']).encode('UTF8'),
																  node_code=j['node_code'],
																  pe_code=j['pe_code'],
																  pe_type=j['pe_type'],
																  pe_default_port_ip=j['pe_default_port_ip'],
																  pe_vlan_port_ip=j['pe_vlan_port_ip'],
																  pe_vpn_server_ip=pe_access_ser_ip,
																  pe_vpn_ip_range_start=pe_access_pool_start,
																  pe_vpn_ip_range_end=pe_access_pool_end,
																  pe_vpn_access_port=pe_access_port,
																  virtual_network_number=virt_port_no)
							self._storage_controller.run(ins)
		self._update_pe_total_table_md5sum()
		return False

	def list_boss_ce_endpoint(self):
		http = httplib2.Http()
		timestamp = int(time.time())
		body_dict = {'query_id': timestamp, 'customer_id': '', 'customer_code': '', 'virtual_network_number': ''}
		ce_list_result = utils.make_notify(body_dict, self._conf.boss_business_config_url)
		result_dict = {}
		try:
			result_dict = jsonutils.loads(ce_list_result)
		except ValueError as e:
			LOG.exception(e)
			
		self._ce_list_result = result_dict

	def format_ce_list_result(self):
		access_instance_list =  []
		if self._ce_list_result:
			data_list = self._ce_list_result['data_list']
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
						access_instance_dict['vpn_cli_ip'] = k['client_ip']
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
			self._ce_row_list = access_instance_list
			ce_table_md5 = ''
			for i in self._ce_row_list:
				ce_table_md5 += i['ce_row_md5sum']
			ce_table_md5sum = utils.md5sum(ce_table_md5)
			for i in self._ce_row_list:
				i['ce_table_md5sum'] = ce_table_md5sum

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
		self._listed_ce_count = len(self._ce_row_list)

		sel = sa.sql.select(select_fields)
		result = self._storage_controller.run(sel)
		
		if self._selected_ce_count is self._listed_ce_count:
			for i, v in enumerate(result):
				LOG.debug(u'Ce total md5hashchecksum from local db :%s', v['ce_table_md5sum'])
				LOG.debug(u'Ce total md5hashchecksum from BOSS:%s', self._ce_row_list[i]['ce_table_md5sum'])
				if v['ce_table_md5sum'] == self._ce_row_list[i]['ce_table_md5sum']:
					LOG.debug(u'Same result. Ce Synchronization finished.')
					return True

		sel_md5_lst = []
		lis_md5_lst = []
		sel = sa.sql.select(select_fields)
		result = self._storage_controller.run(sel)
		if self._listed_ce_count:
			for i in result:
				sel_md5_lst.append(i['ce_row_md5sum'])

		for j in self._ce_row_list:
			lis_md5_lst.append(j['ce_row_md5sum'])
		
		#print sel_md5_lst
		#print lis_md5_lst
		
		for i in sel_md5_lst:
			if i not in lis_md5_lst:
				sel = sa.sql.select([tables.Ce_total.c.username,
				                     tables.Ce_total.c.password,
				                     tables.Ce_total.c.vpn_cli_ip,
				                     tables.Ce_total.c.pe_code,
				                     tables.Ce_total.c.ce_row_md5sum,
				                     tables.Ce_total.c.access_instance_id], 
									 tables.Ce_total.c.ce_row_md5sum == i)
				result = self._storage_controller.run(sel)
				access_id_del = 0
				for j in result:
					self.looping_call_agent(dict(j), 'delete')
					self._notify_list_delete.append(j['access_instance_id'])
					access_id_del = j['access_instance_id']
				de = tables.Ce_total.delete().where(tables.Ce_total.c.ce_row_md5sum == i)
				self._storage_controller.run(de)
				de = tables.Ce.delete().where(tables.Ce.c.access_instance_id == access_id_del)
				self._storage_controller.run(de)
		self._update_ce_total_table_md5sum()

		for i in lis_md5_lst:
			if i not in sel_md5_lst:
				for j in self._ce_row_list:
					if j['ce_row_md5sum'] == i:
						LOG.debug(u'Looping call agent. access_instance_id:%d', j['access_instance_id'])
						self.looping_call_agent(dict(j), 'create')
						self._notify_list_create.append(j['access_instance_id'])
						LOG.debug(u'Get pe_code=%d', j['pe_code']
						sel = sa.sql.select([tables.Pe.c.id], tables.Pe.c.pe_code == j['pe_code'])
						result = self._storage_controller.run(sel)
						if result.rowcount:
							for k in result:
								pe_id = k['id']
							ins = sa.sql.expression.insert(tables.Ce).values(virtual_network_number=j['virtual_network_number'],
								                                             customer_id=j['customer_id'],
																			 customer_code=j['customer_code'],
																			 access_instance_id=j['access_instance_id'],
																			 tunnel_type=j['tunnel_type'],
																			 vpn_cli_ip=j['vpn_cli_ip'],
																			 username=j['username'],
																			 password=j['password'],
																			 work_mode=j['work_mode'],
																			 pe_id=pe_id)
							self._storage_controller.run(ins)
							ins = sa.sql.expression.insert(tables.Ce_total).values(ce_row_md5sum=j['ce_row_md5sum'],
								                                                   ce_table_md5sum=j['ce_table_md5sum'],
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
							self._storage_controller.run(ins)
		self._update_ce_total_table_md5sum()

	def _update_pe_total_table_md5sum(self):
		sel = sa.sql.select([tables.Pe_total.c.pe_row_md5sum])
		result = self._storage_controller.run(sel)
		pe_table_md5sum = ''
		for i in result:
			pe_table_md5sum += i['pe_row_md5sum']
		pe_table_md5sum_value = utils.md5sum(pe_table_md5sum)
		stmt = tables.Pe_total.update().values(pe_table_md5sum=pe_table_md5sum_value)
		self._storage_controller.run(stmt)
		self._storage_controller.close()

	def _update_ce_total_table_md5sum(self):
		sel = sa.sql.select([tables.Ce_total.c.ce_row_md5sum])
		result = self._storage_controller.run(sel)
		ce_table_md5sum = ''
		for i in result:
			ce_table_md5sum += i['ce_row_md5sum']
		ce_table_md5sum_value = utils.md5sum(ce_table_md5sum)
		stmt = tables.Ce_total.update().values(ce_table_md5sum=ce_table_md5sum_value)
		self._storage_controller.run(stmt)
		self._storage_controller.close()
