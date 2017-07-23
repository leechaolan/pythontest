from oslo_config import cfg
from oslo_log import log
import bootstrap
#from transport.wsgi import driver
#from storage import controller

conf = cfg.CONF
log.register_options(conf)
conf(project='pythontest', prog='pythontest-user', args=[])
#conf(defualt_config_files='/etc/pythontest.conf')
log.setup(conf, 'pythontest')

boot = bootstrap.Bootstrap(conf)
conf.drivers.transport = 'wsgi'

application = boot.transport()
app = application.app
