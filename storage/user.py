from oslo_log import log
import sqlalchemy as sa
import storage
from storage import tables
from storage import utils

LOG = log.getLogger(__name__)

class UserController(storage.User):

	def _list(self, project_id=None):

		if project_id is None:
			project_id = ''
	
		node_fields = [tables.Node.c.node_id,
		               tables.Node.c.node_code]
		host_fields = [tables.Host.c.host_id,
		               tables.Host.c.host_code,
					   tables.Host.c.host_type,
		               tables.Host.c.host_work_status]
		pe_fields = [tables.Pe.c.id,
		             tables.Pe.c.pe_code,
		             tables.Pe.c.pe_type,
		             tables.Pe.c.pe_work_status]

		sel = sa.sql.select(node_fields)
		nodes = self.driver.run(sel)
		node_code = []
		host_list = []
		index = 0

		for i in nodes:
			node_code.append(i['node_code'])
			host_list.append([])
		nolst = [{'node_code': c, 'host_list': l} for c, l in zip(node_code, host_list)]

		sel = sa.sql.select(node_fields)
		nodes = self.driver.run(sel)
		index = 0
		for i in nodes:
			sel = sa.sql.select(host_fields, tables.Host.c.node_id == i['node_id'])
			rec = self.driver.run(sel)
			host_code = []
			host_type = []
			host_work_status = []
			for j in rec:
				host_code.append(j['host_code'])
				host_type.append(j['host_type'])
				host_work_status.append(j['host_work_status'])
			holst = [{'host_code': c, 'host_type': t, 'host_work_status': w} for c, t, w in zip(host_code, host_type, host_work_status)]
			nolst[index]['host_list'] = holst
			index += 1

		sel = sa.sql.select(node_fields)
		nodes = self.driver.run(sel)
		index_i = 0
		for i in nodes:
			sel = sa.sql.select(host_fields, tables.Host.c.node_id == i['node_id'])
			rec = self.driver.run(sel)
			index_j = 0
			for j in rec:
				sel = sa.sql.select(pe_fields, tables.Pe.c.host_id == j['host_id'])
				precs = self.driver.run(sel)
				pe_code = []
				pe_type = []
				pe_work_status = []
				for k in precs:
					pe_code.append(k['pe_code'])
					pe_type.append(k['pe_type'])
					pe_work_status.append(k['pe_work_status'])
				pelst = [{'pe_code': c, 'pe_type': t, 'pe_work_status': w} for c, t, w in zip(pe_code, pe_type, pe_work_status)]
				nolst[index_i]['host_list'][index_j]['pe_list'] = pelst
				index_j += 1
			index_i += 1
			
		response_body = {'result': 1, 'error_code': 0, 'error_msg': ''}
		response_body['data_list'] = nolst
		print response_body

#		sel = sel.group_by(sa.asc(tables.Node.c.node_code)).limit(10)

		return response_body

#		def it():
#			for rec in records:
#				marker_name['next'] = rec[0]
#				yield({'node_code': rec[0]})
#
#		yield it()
#		yield marker_name and marker_name['next']

	def _get(self, name, project_id=None):
		print '-------------------get this--------------'
		print '-------------------get this--------------'
		print '-------------------get this--------------'
		print 'UserController self.driver %s' % self.driver
		return {}
