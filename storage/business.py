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

		pe_fields = [tables.Pe.c.pe_code,
		             tables.Pe.c.pe_vpn_server_ip,
		             tables.Pe.c.pe_vpn_access_port]
		ce_fields = [tables.Ce.c.id,
		             tables.Ce.c.customer_id,
		             tables.Ce.c.customer_code,
		             tables.Ce.c.virtual_network_number,
		             tables.Ce.c.access_instance_id,
		             tables.Ce.c.work_mode,
		             tables.Ce.c.tunnel_type,
					 tables.Ce.c.vpn_cli_ip,
					 tables.Ce.c.username,
					 tables.Ce.c.password]

		sel = sa.sql.select(tables.Ce.c.customer_id, tables.Ce.c.customer_code)
		ces = self.driver.run(sel)
		customer_id = []
		customer_code = []
		vnetid = []

		for i in ces:
			customer_id.append(i['customer_id'])
			customer_code.append(i['customer_code'])
			vnet_list.append([])
		celst = [{'customer_id': i, 'customer_code': c} for i, c in zip(customer_id, customer_code)]

		sel = sa.sql.select(tables.Ce.c.customer_id, tables.Ce.c.customer_code)
		ces = self.driver.run(sel)
		index = 0
		for i in ces:
			vnetid = []
			access_ins_lst = []
			sel = sa.sql.select(tables.Ce.c.virtual_network_id, tables.Ce.c.customer_id == i['customer_id'])
			res = self.driver.run(sel)
			for j in ces:
				vnetid.append(j['virtual_network_number'])
			vnet_id_lst = [{'virtual_network_number': n} for n in zip(vnetid)]
			celst[index]['virtual_network_list'] = vnet_id_lst
			index += 1

		sel = sa.sql.select(tables.Ce.c.customer_id, tables.Ce.c.customer_code)
		ces = self.driver.run(sel)
		for i in ces:
			sel = sa.sql.select(tables.Ce.c.virtual_network_id, tables.Ce.c.customer_id == i['customer_id'])
			res = self.driver.run(sel)
			for j in ces:
				sel = sa.sql.select(ce_fields, tables.Ce.c.virtual_network_number == j['virtual_network_number'])
				precs = self.driver.run(sel)
				ins_id = []
				pe_code = []
				

	

		return {}

#		def it():
#			for rec in records:
#				marker_name['next'] = rec[0]
#				yield({'node_code': rec[0]})
#
#		yield it()
#		yield marker_name and marker_name['next']
