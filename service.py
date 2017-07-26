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

	def __init__(self, conf, storage):
		self._conf = conf
		self._storage = storage
		self.list_result = {}

	def invoke_boss_endpoint_list(self):
		http = httplib2.Http()
		timestamp = int(time.time())
		body_dict = {'query_id': timestamp, 'node_code': '', 'host_code': '', 'pe_code': ''}
		resp, context = http.request(self._conf.boss_operate_uri,
				               method="POST",
							   headers={'Context-Type': 'application/x-www-form-urlencoded'},
							   body=urllib.urlencode(body_dict))
		self.list_result = context.decode()

	def contrast_to_local_db(self):
		# First compare each item count.
		# If count different chanage it refer to result from BOSS
		LOG.debug(u'begin contrast between local db and result from invoke BOSS list endpoint')
		list_result_decode = jsonutils.loads(self.list_result)
		self._list_result_decode = list_result_decode
		print self._list_result_decode

		node_count = len(self._list_result_decode['data_list'])
		node_list = self._list_result_decode['data_list']
		sel = sa.sql.select([func.count()]).select_from(tables.Node)
		result = self._storage.run(sel)
		select_count = int(result.fetchone()[0])
		for i in node_list:
			host_count = len(i['host_list'])
			host_list = i['host_list']
			print('host_list: {0}, count:{1}'.format(host_list, host_count))
			sel = sa.sql.select([func.count()]).select_from(tables.Host)
			result = self._storage.run(sel)
			select_count = int(result.fetchone()[0])
			for j in host_list:
				if 'pe_list' in j:
					pe_list = j['pe_list']
					pe_count = len(j['pe_list'])
					print('pe_list: {0}, count:{1}'.format(pe_list, pe_count))
					sel = sa.sql.select([func.count()]).select_from(tables.Pe)
					result = self._storage.run(sel)
					select_count = int(result.fetchone()[0])

		
		sel = sa.sql.select([tables.Pe_total.c.pe_md5sum_md5sum])
		result = self._storage.run(sel)
		pe_table_md5sum = int(result.fetchone()[0])
