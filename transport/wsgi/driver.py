from oslo_log import log
import six
from oslo_config import cfg
import falcon
from transport.wsgi import user
from transport.wsgi import business
from transport.wsgi import cfg_notify
from transport.wsgi import manualsync
import transport

LOG = log.getLogger(__name__)

class Driver(transport.DriverBase):

	def __init__(self, conf, storage):
		super(Driver, self).__init__(conf, storage)
		self._conf.register_opts(_WSGI_OPTIONS, group=_WSGI_GROUP)
		self._wsgi_conf = self._conf[_WSGI_GROUP]
		self.app = None
		self._init_routes()

	def _init_routes(self):
		endpoints = [('/operation_status_query', user.ItemResource(self._storage.user_controller)),
		             ('/business_deploy_query', business.ItemResource(self._storage.business_controller)),
		             ('/business_config_notify', cfg_notify.ItemResource(self._conf, self._storage.cfg_notify_controller)),
		             ('/manual_sync', manualsync.ItemResource(self._conf, self._storage.mansync_controller))]
		self.app = falcon.API()
		self.app.add_error_handler(Exception, self._error_handler)
		for route, resource in endpoints:
			self.app.add_route(route, resource)

	def _error_handler(self, exc, request, response, params):
		if isinstance(exc, falcon.HTTPError):
			raise exc
		LOG.exception(exc)
		raise falcon.HTTPInternalServerError('Internal server error',
				                             six.text_type(exc))


_WSGI_OPTIONS = (
	cfg.HostAddressOpt('bind', default='127.0.0.1',
		               help='Address on which the self-hosting server will '
					        'listen.'),
	cfg.PortOpt('prot', default=9000,
		        help='Port on which the self-hosting server will listen.'),
)

_WSGI_GROUP = 'drivers:transport:wsgi'


def _config_options():
	return [(_WSGI_GROUP, _WSGI_OPTIONS)]

#endpoints = [('/users', user.ItemResource(controller=None))]
#app = falcon.API()
#for route, resource in endpoints:
#	app.add_route(route, resource)


#driver = Driver(conf=None)
#app = driver.app
