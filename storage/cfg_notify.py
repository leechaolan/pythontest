import time
from oslo_log import log
import sqlalchemy as sa
import storage
from storage import tables
from storage import utils

LOG = log.getLogger(__name__)

class CfgNotifyController(storage.CfgNotify):
	
	def get_pe_ip(self, pe_code):
		sel_field = [tables.Pe.c.pe_default_port_ip]
		sel = sq.sql.select(sel_field, tables.Pe.c.pe_code == pe_code)
		result = self.driver.run(sel)

		for i in result:
			pe_ip = i['pe_default_port_ip']
			return pe_ip

	def get_agent_ip(self, pe_code):
		sel_field = [tables.Ce.c.pe_id, 
		             tables.Pe.c.host_id,
	                 tables.Host.c.host_ip_address]
		sel = sa.sql.select(sel_field, 
				            tables.Pe.c.pe_code == pe_code).select_from(tables.Ce.join(tables.Pe, 
									                                                   tables.Ce.c.pe_id == tables.Pe.c.id))
		result = self.driver.run(sel)
		for i in result:
			print i['host_ip_address']
			host_ip = i['host_ip_address']
			return host_ip

	def create_user_to_agent(self, payload):
		ip = self.get_agent_ip(payload['pe_code'])
		pe_ip = self.get_pe_ip(payload['pe_code'])
		payload['pe_ip'] = pe_ip
		url = 'http://' + ip + ':' + 9001 + '/users'
		resp = utils.make_notify(payload, url)
		return resp['result']

	def _list(self, result_dict, project_id=None):
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
		pass
		print access_instance_list
		print access_instance_id_list

		sel_access_list = []
		sel = sa.sql.select([tables.Ce.c.access_instance_id])
		result = self.driver.run(sel)
		for i in result:
			sel_access_list.append(i['access_instance_id'])

		for i in access_instance_id_list:
			if i not in sel_access_list:
				for j in access_instance_list:
					if j['access_instance_id'] == i:
						instance_dict = dict(j)
						result = False
						while (result is not True):
							result = create_user_to_agent(instance_dict)
							time.sleep(20)
						sel = sa.sql.select([tables.Pe.c.pe_id], tables.Pe.c.pd_code == j['pe_code'])
						result = self.driver.run(sel)
						for k in result:
							pe_id = k['pe_id']
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

						self._storage_controller.run(ins)
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

						self._storage_controller.run(ins)
						sel = sq.sql.select([tables.Ce_total.c.ce_table_md5sum])
						result = self.driver.run(sel)
						ce_table_md5sum = ''
						for i in result:
							ce_table_md5sum += i['ce_row_md5sum']
						ce_table_md5sum_value = utils.md5sum(ce_table_md5sum)
						stmt = tables.Ce_total.update().values(ce_table_md5sum=ce_table_md5sum_value)
						self.driver.run(stmt)

	def make_user_payload(self, access_instance_id):
		pass
