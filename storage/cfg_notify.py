import time
import threading
from oslo_log import log
from oslo_serialization import jsonutils
import sqlalchemy as sa
import storage
from storage import tables
from storage import utils

LOG = log.getLogger(__name__)

class CfgNotifyController(storage.CfgNotify):

	def notify_boss(self):
		notify_id = time.time()
		notify_dic = {'query_id': notify_id}
		body = jsonutils.loads(notify_dic)
		LOG.debug(u'Notify BOSS that config is done. body:%(body)s boss_url:%(boss_url)',
				  {'body': body, 'boss_url': self._boss_url})
		make_notify(body, self._boss_url)

	def looping_call_agent(self, payload, method):
		LOG.debug(u'self._notify_list_create is %s', self._notify_list_create)
		LOG.debug(u'self._notify_list_delete is %s', self._notify_list_delete)
		default_call_interval = 30
		args = []
		args.append(payload)
		args.append(method)
		t = threading.Timer(default_call_interval, self.looping_call_agent, args)
		t.daemon = True
		t.start()
		result = self.to_agent(payload, method)

		if result is 1:
			t.cancel()
			if method is 'create':
				self._notify_list_create.remove(payload['access_instance_id'])
			if method is 'delete':
				self._notify_list_delete.remove(payload['access_instance_id'])
				
		if self._notify_list_create is [] or self._notify_list_delete is []:
			self.notify_boss()

	def get_pe_ip(self, pe_code):
		sel_field = [tables.Pe.c.pe_default_port_ip]
		sel = sa.sql.select(sel_field, tables.Pe.c.pe_code == pe_code)
		result = self.driver.run(sel)
	
		if result.rowcount:
			for i in result:
				pe_ip = i['pe_default_port_ip']
			return pe_ip
		else:
			return ''

	def get_agent_ip(self, pe_code):
		sel_field = [tables.Ce.c.pe_id, 
		             tables.Pe.c.host_id,
	                 tables.Host.c.host_ip_address]
		sel = sa.sql.select(sel_field, 
				            tables.Pe.c.pe_code == pe_code).select_from(tables.Ce.join(tables.Pe, 
									                                                   tables.Ce.c.pe_id == tables.Pe.c.id))
		result = self.driver.run(sel)
		if result.rowcount:
			for i in result:
				host_ip = i['host_ip_address']
			return host_ip
		else:
			return ''

	def to_agent(self, payload, method):
		ip = self.get_agent_ip(payload['pe_code'])
		pe_ip = self.get_pe_ip(payload['pe_code'])
		LOG.debug(u'agent_ip=%s, pe_ip=%s', ip, pe_ip)
		payload['method'] = method
		LOG.debug(u'payload=%s, method=%s', payload, method)

		if ip and pe_ip:
			payload['pe_ip'] = pe_ip
			url = 'http://' + str(ip) + ':' + '9001' + '/users'
			LOG.debug(u'url=%s', url)
			resp = utils.make_notify(payload, url)
			return resp['result']
		else:
			LOG.error(u'agent ip or pe_ip is none')
			return ''

	def _list(self, result_dict, boss_url, project_id=None):
		# save boss URL first
		self._boss_url = boss_url 
		access_instance_list =  []
		access_instance_id_list = []
		customer_code = result_dict['data_list'][0]['customer_code']
		customer_id = result_dict['data_list'][0]['customer_id']
		vnetwork_list = result_dict['data_list'][0]['virtual_network_list']
		for i in vnetwork_list:
			instance = i['access_instance_list']
			for j in instance:
				access_instance_dict = {}
				access_instance_dict['virtual_network_number'] = i['virtual_network_number']
				access_instance_dict['access_instance_id'] = j['access_instance_id']
				access_instance_dict['openvpn_client_ip'] = j['openvpn_client_ip']
				access_instance_dict['password'] = j['password']
				access_instance_dict['pe_code'] = j['pe_code']
				access_instance_dict['tunnel_type'] = j['tunnel_type']
				access_instance_dict['username'] = j['username']
				access_instance_dict['work_mode'] = j['work_mode']
				access_instance_list.append(access_instance_dict)
				access_instance_id_list.append(j['access_instance_id'])

		print access_instance_list
		print access_instance_id_list

		sel_access_list = []
		sel = sa.sql.select([tables.Ce.c.access_instance_id])
		result = self.driver.run(sel)
		for i in result:
			sel_access_list.append(i['access_instance_id'])

		self._notify_list = []
		for i in access_instance_id_list:
			if i not in sel_access_list:
				for j in access_instance_list:
					if j['access_instance_id'] == i:
						self._notify_list_create.append(j['access_instance_id'])
						self.looping_call_agent(dict(j), 'create')
						sel = sa.sql.select([tables.Pe.c.id], tables.Pe.c.pe_code == j['pe_code'])
						result = self.driver.run(sel)
						pe_id = 0
						for k in result:
							pe_id = k['pe_id']
						if pe_id:
							ins = sa.sql.expression.insert(tables.Ce).values(virtual_network_number=j['virtual_network_number'],
									                                         customer_id=customer_id,
																			 customer_code=customer_code,
																			 access_instance_id=j['access_instance_id'],
																			 tunnel_type=j['tunnel_type'],
																			 vpn_cli_ip=j['openvpn_client_ip'],
																			 username=j['username'],
																			 password=j['password'],
																			 work_mode=j['work_mode'],
																			 pe_id=pe_id)

							self.driver.run(ins)
							ce_row_md5 = j['virtual_network_number'] + customer_id + customer_code +\
							             j['access_instance_id'] + j['tunnel_type'] + j['openvpn_client_ip'] +\
										 j['username'] + j['password'] + j['work_mode'] + j['pe_code']
							ce_row_md5_val = utils.md5sum(ce_row_md5)
							
							ins = sa.sql.expression.insert(tables.Ce_total).values(ce_row_md5sum=ce_row_md5_val,
									                                               virtual_network_number=j['virtual_network_number'],
																				   customer_id=customer_id,
																				   customer_code=customer_code,
																				   access_instance_id=j['access_instance_id'],
																				   tunnel_type=j['tunnel_type'],
																				   vpn_cli_ip=j['vpn_cli_ip'],
																				   username=j['username'],
																				   password=j['password'],
																				   pe=j['pe_code'])

							self.driver.run(ins)
		self.update_ce_total_table_md5sum()

		for i in sel_access_list:
			if i not in access_instance_id_list:
				select_field = [tables.Ce.c.virtual_network_number,
				                tables.Ce.c.access_instance_id,
				                tables.Ce.c.openvpn_client_ip,
				                tables.Ce.c.password,
				                tables.Ce.c.pe_code,
				                tables.Ce.c.tunnel_type,
				                tables.Ce.c.username,
				                tables.Ce.c.work_mode]
				sel = sq.sql.select(select_field, tables.Ce.c.access_instance_id == i)
				result = self.driver.run(sel)
				for j in result:
					sel_access_ins_dict = {}
					sel_access_ins_dict.append(j['virtual_network_number'])
					sel_access_ins_dict.append(j['access_instance_id'])
					sel_access_ins_dict.append(j['openvpn_client_ip'])
					sel_access_ins_dict.append(j['password'])
					sel_access_ins_dict.append(j['pe_code'])
					sel_access_ins_dict.append(j['tunnel_type'])
					sel_access_ins_dict.append(j['username'])
					sel_access_ins_dict.append(j['work_mode'])
					self._notify_list_delete.append(j['access_instance_id'])
					self.looping_call_agent_delete(sel_access_ins_dict, 'delete')
					de = tables.Ce_total.delete().where(tables.Ce_total.access_instance_id == j['access_instance_id'])
					self._storage_controller.run(de)
					de = tables.Ce.delete().where(tables.Ce.c.access_instance_id == j['access_instance_id'])
					self._storage_controller.run(e)
		self.update_ce_total_table_md5sum()

	def _update_pe_total_table_md5sum(self):
		sel = sq.sql.select([tables.Pe_total.c.pe_row_md5sum])
		result = self.driver.run(sel)
		pe_table_md5sum = ''
		for i in result:
			pe_table_md5sum += i['pe_row_md5sum']
		pe_table_md5sum_value = utils.md5sum(pe_table_md5sum)
		stmt = tables.Pe_total.update().values(pe_table_md5sum=pe_table_md5sum_value)
		self.driver.run(stmt)
		self.driver.close()

	def _update_ce_total_table_md5sum(self):
		sel = sq.sql.select([tables.Ce_total.c.ce_row_md5sum])
		result = self.driver.run(sel)
		ce_table_md5sum = ''
		for i in result:
			ce_table_md5sum += i['ce_row_md5sum']
		ce_table_md5sum_value = utils.md5sum(ce_table_md5sum)
		stmt = tables.Ce_total.update().values(ce_table_md5sum=ce_table_md5sum_value)
		self.driver.run(stmt)
		self.driver.close()
