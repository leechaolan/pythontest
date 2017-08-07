from oslo_log import log
import sqlalchemy as sa
import storage
from storage import tables
from storage import utils

LOG = log.getLogger(__name__)

class BusinessController(storage.Business):

	def _list(self, project_id=None):

		if project_id is None:
			project_id = ''

		ins_list_fields = [tables.Ce.c.access_instance_id,
		                   tables.Ce.c.work_mode,
		                   tables.Ce.c.tunnel_type,
						   tables.Ce.c.vpn_cli_ip,
						   tables.Ce.c.username,
						   tables.Ce.c.password,
		                   tables.Pe.c.pe_code,
						   tables.Pe.c.pe_vpn_server_ip,
						   tables.Pe.c.pe_vpn_access_port
						   ]


		sel = sa.sql.select([tables.Ce.c.customer_id, tables.Ce.c.customer_code])
		ces = self.driver.run(sel)
		datalist = []
		result_dict = {}

		for i in ces:
			datalist_dic = {}
			datalist_dic['customer_id'] = i['customer_id']
			datalist_dic['customer_code'] = i['customer_code']
			virtual_network_lst = []
			sel = sa.sql.select(tables.Ce.c.virtual_network_id, tables.Ce.c.customer_i == i['customer_id'])
			result = self.driver.run(sel)
			for j in result:
				vnet_dict = {}
				vnet_dict['virtual_network_number'] = j['virtual_network_number']
				sel = sa.sql.select(ins_list_fields, 
						            tables.Ce.c.virtual_network_number == j['virtual_network_number']).select_from(tables.Pe.join(tables.Ce, tables.Ce.c.pe_id == tables.Pe.c.id))
				result = self.driver.run(sel)
				access_instance_lst = []
				for k in result:
					instance_list_dict = {}
					instance_list['access_instance_id'] = k['access_instance_id']
					instance_list['pe_code'] = k['pe_code']
					instance_list['work_mode'] = k['work_mode']
					instance_list['tunnel_type'] = k['tunnel_type']
					instance_list['access_server_ip'] = k['pe_vpn_server_ip']
					instance_list['access_server_port'] = k['pe_vpn_access_port']
					instance_list['openvpn_client_ip'] = k['vpn_cli_ip']
					instance_list['username'] = k['username']
					instance_list['password'] = k['password']
					access_instance_lst.append(instance_list_dict)
				vnet_dict['access_instance_list'] = access_instance_lst
				virtual_network_lst.append(vnet_dict)
			customer_dic['virtual_network_list'] = virtual_network_lst
			datalist.append(datalist_dic)
	
		result_dict['data_list'] = datalist
		result_dict['error_code'] = 1
		result_dict['error_msg'] = ''
		result_dict['result'] = 1


		return result_dict

#		def it():
#			for rec in records:
#				marker_name['next'] = rec[0]
#				yield({'node_code': rec[0]})
#
#		yield it()
#		yield marker_name and marker_name['next']
