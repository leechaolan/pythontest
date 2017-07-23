from oslo_service import loopingcall

class Service(object):

	def __init__(self, conf):
		self.conf = conf
		self.periodic_interval = conf.periodic_task_interval
		self.timers = []
		self.start()

	def start(self):
		if self.conf.periodic_task_interval is None:
			self.periodic_interval = 60*60*24
		
		periodic = loopingcall.DynamicLoopingCall(
			self.periodic_task)
		periodic.start(periodic_interval_max=self.periodic_interval,
				       initial_delay=None).wait()
		self.timers.append(periodic)

	def periodic_task(self):
		print 'periodic is called!'
		return True
