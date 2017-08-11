import time
import httplib2
import urllib
from oslo_log import log
from oslo_serialization import jsonutils
import falcon
import json
from storage import utils

LOG = log.getLogger(__name__)

class ItemResource(object):
	__slots__ = ('_conf', '_cfg_notify_controller')

	def __init__(self, conf, cfg_notify_controller):
		self._cfg_notify_controller = cfg_notify_controller
		self._conf = conf

	def on_post(self, req, resp):
		if req.content_length:
			doc = json.load(req.stream)
		print doc
		resp.status = falcon.HTTP_200
		resp.body = '{"result": 1, "error_code": 0, "error_msg": ""}'
		http = httplib2.Http()
		timestamp = int(time.time())
		body_dict = {'query_id': timestamp, 'customer_id': 1, 'custome_code': '', 'virtual_network_number': ''}
		resp_for_list, context = http.request(self._conf.boss_business_config_url,
				                              method="POST",
											  headers={'Context-Type': 'application/x-www-form-urlencoded'},
											  body=urllib.urlencode(body_dict))
		list_result = context.decode()
		result_dict = jsonutils.loads(list_result)
		notify_boss_url = self._conf.boss_deploy_url
		self._cfg_notify_controller.list(result_dict, notify_boss_url, project_id=None)

