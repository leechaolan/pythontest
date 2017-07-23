from oslo_log import log
import falcon
import json
from storage import utils

LOG = log.getLogger(__name__)

class ItemResource(object):
	__slots__ = ('_business_controller')

	def __init__(self, business_controller):
		self._business_controller = business_controller

	def on_get(self, req, resp):
		#resp_dict = self._business_controller.get(name=None, project_id=None)
		pass

	def on_put(self, req, resp):
		pass

	def on_post(self, req, resp):
		resp.status = falcon.HTTP_200
		print '=========================== Business called !============='
		response_body = self._business_controller.list(project_id=None)
		res = {}
		resp.body = utils.to_json(res)
