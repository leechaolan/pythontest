from oslo_config import cfg
from oslo_log import log
import bootstrap
import os
import service

conf = cfg.CONF
log.register_options(conf)
conf(project='pythontest', prog='pythontest-user', args=[])
#conf(defualt_config_files='/etc/pythontest.conf')
log.setup(conf, 'pythontest')

boot = bootstrap.Bootstrap(conf)
conf.drivers.transport = 'wsgi'
application = boot.transport()
app = application.app
periodic_task = service.Periodic_Task(conf, boot._storage)

import time, threading
def run_periodic_task():
	#threading.Thread.daemon = True
	#if conf.periodic_task_interval is None:
		#interval = 60*60*24
	periodic_task.list_boss_pe_endpointt()
	periodic_task.format_pe_list_result()
	periodic_task.pe_contrast_to_local_db()
	#periodic_task.list_boss_ce_endpoint()
	#periodic_task.format_ce_list_result()
	#periodic_task.ce_contrast_to_local_db()
	#interval = conf.periodic_task_interval
	#t = threading.Timer(interval, run_periodic_task)
	#t.start()
	#t.cancel()
run_periodic_task()
