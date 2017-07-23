from oslo_log import log
import falcon
import json
from storage import utils

LOG = log.getLogger(__name__)

class ItemResource(object):
	__slots__ = ('_user_controller')

	def __init__(self, user_controller):
		self._user_controller = user_controller

	def on_get(self, req, resp):
		resp.status = falcon.HTTP_200
		print '=========================== called !============='
		#_resp_dict = self._user_controller.get(name=None, project_id=None)
		response_body = self._user_controller.list(project_id=None)
#response_body = {'data_list': [{'node_code': 'bj01', 'host_list': [{'host_code': 'gw01', 'host_work_status': 'normal', 'pe_list': [{'pe_code': '01', 'pe_type': 'public'}]}]}]}
		#test_list = [[], []]
		#print test_list
		#for i in results:
			#print i.node_code
		
		resp.body = utils.to_json(response_body)

	def on_put(self, req, resp):
		pass

	def on_post(self, req, resp):
		resp.status = falcon.HTTP_200
		resp.body = 'test'
