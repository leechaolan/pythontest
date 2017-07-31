from oslo_log import log
import falcon
import json

LOG = log.getLogger(__name__)

class ItemResource(object):

	def __init__(self, conf):
		self._conf = conf

	def on_get(self, req, resp):
		resp.status = falcon.HTTP_200
		print '=========================== called !============='
		response_body = self._user_controller.list(project_id=None)
		#resp.body = utils.to_json(response_body)

	def on_put(self, req, resp):
		pass

	def on_post(self, req, resp):
		resp.status = falcon.HTTP_200
		resp.body = 'nmc-agent'
