from oslo_config import cfg
from oslo_log import log
import bootstrap
import service
#from transport.wsgi import driver
#from storage import controller

conf = cfg.CONF
log.register_options(conf)
conf(project='pythontest', prog='pythontest-user', args=[])
#conf(defualt_config_files='/etc/pythontest.conf')
log.setup(conf, 'pythontest')

boot = bootstrap.Bootstrap(conf)
conf.drivers.transport = 'wsgi'
#print('Invoke BOSS list-endpoint interval is %d' % conf.periodic_task_interval)

application = boot.transport()
app = application.app
#service.Service(conf)
def periodic_task():
	pass
