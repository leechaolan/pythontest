import time
from oslo_log import log
import sqlalchemy as sa
import storage
from storage import tables
from storage import utils

LOG = log.getLogger(__name__)

class CfgNotifyController(storage.CfgNotify):

	def get_agent_ip(self, pe_code):
		sel_field = []
		sel_access_list = []
		sel_field = ([tables.Ce.c.pe_id, 
				      tables.Pe.c.host_id,
					  tables.Host.c.host_ip_address])
		sel = sa.sql.select(sel_field, 
				            tables.Pe.c.pe_code == pe_code).select_from(tables.Ce.join(tables.Pe, 
									                                                   tables.Ce.c.pe_id == tables.Pe.c.id))
		result = self.driver.run(sel)
		for i in result:
			print i['host_ip_address']
			host_ip = i['host_ip_address']
			return host_ip
		pass

	def create_user_to_agent(self, payload):
		ip = self.get_agent_ip(payload['pe_code'])
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

	def make_user_payload(self, access_instance_id):
		pass
