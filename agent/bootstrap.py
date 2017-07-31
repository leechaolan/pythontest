from oslo_log import log
from stevedore import driver
import bootstrap
from common import consts
from common import errors
from common import configs

LOG = log.getLogger(__name__)

class Bootstrap(object):

	def __init__(self, conf):
		self.conf = conf

		for group, opts in configs._config_options():
			self.conf.register_opts(opts, group=group)

		self.driver_conf = self.conf[configs._DRIVER_GROUP]
		#self._storage = self.storage()

	def api(self):
		LOG.debug(u'Loading API handler')
		return handler.Handler(self._storage)

	def transport(self):
		transport_name = self.driver_conf.transport
		LOG.debug(u'Loading transport driver: %s', transport_name)

		#args = [self.conf, self._storage,]
		args = [self.conf,]

		try:
			mgr = driver.DriverManager('nmc_agent.transport',
					                   transport_name,
									   invoke_on_load=True,
									   invoke_args=args)
			return mgr.driver
		except RuntimeError as exc:
			LOG.exception(exc)
			LOG.error(u'Failed to load transport driver nmc_agent.transport.'
					  u'%(driver)s with args %(args)s',
					  {'driver': transport_name, 'args': args})
			raise errors.InvalidDriver(exc)
