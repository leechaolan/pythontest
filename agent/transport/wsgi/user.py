from oslo_log import log
import falcon
import json
from libvirt import guest
from common import configs
from transport.wsgi import utils

LOG = log.getLogger(__name__)

class ItemResource(object):

	def __init__(self, conf):
		self._conf = conf

	def on_get(self, req, resp):
		resp.status = falcon.HTTP_200
		resp.body = ''

	def on_put(self, req, resp):
		pass

	def on_post(self, req, resp):
		domname = req.stream['pe_code']
		username = req.stream['username']
		password = req.stream['password']
		userip = req.stream['openvpn_client_ip']
		pe_ip = req.stream['pe_ip']
		result = guest.start_domain(domname)
		utils.add_user(username, password, userip, pe_ip)
		resp.status = falcon.HTTP_200
		if result is False:
			resp.body = '{"result": 0}'
		resp.body = '{"result": 1}'
