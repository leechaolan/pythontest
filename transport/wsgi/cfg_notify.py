from oslo_log import log
import falcon
import json
from storage import utils

LOG = log.getLogger(__name__)

class ItemResource(object):
	__slots__ = ('_cfg_notify_controller')

	def __init__(self, cfg_notify_controller):
		self._cfg_notify_controller = cfg_notify_controller

	def on_post(self, req, resp):
		resp.status = falcon.HTTP_200
		resp.body = 'test_notify'
