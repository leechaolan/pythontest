from oslo_log import log
import falcon
import json
from storage import utils
import service

LOG = log.getLogger(__name__)

class ItemResource(object):
	__slots__ = ('_conf', '_mansync_controller')

	def __init__(self, conf, mansync_controller):
		self._mansync_controller = mansync_controller
		self._conf = conf

	def on_get(self, req, resp):
		resp.status = falcon.HTTP_200
		response_body = self._mansync_controller.list(project_id=None)
		resp.body = utils.to_json(response_body)

	def on_put(self, req, resp):
		pass

	def on_post(self, req, resp):
		resp.status = falcon.HTTP_200
		self._mansync_controller.sync(self._conf)
		response_body = {'result': 1, 'error_code': 0, 'error_msg': ''}
		resp.body = utils.to_json(response_body)
