from oslo_config import cfg
from oslo_log import log
import bootstrap
import os

conf = cfg.CONF
log.register_options(conf)
conf(project='nmc_agent', prog='nmc_agent-user', args=[])
log.setup(conf, 'nmc_agent')

boot = bootstrap.Bootstrap(conf)
conf.drivers.transport = 'wsgi'
application = boot.transport()
app = application.app
