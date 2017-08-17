import six
import abc

class ControllerBase(object):
	
	def __init__(self, driver):
		self.driver = driver

@six.add_metaclass(abc.ABCMeta)
class User(ControllerBase):

	def list(self, project_id=None):
		return self._list(project_id)
	_list = abc.abstractmethod(lambda x: None)

	def get(self, name, project_id=None):
		return self._get(name, project_id)
	_get = abc.abstractmethod(lambda x: None)

@six.add_metaclass(abc.ABCMeta)
class Business(ControllerBase):

	def list(self, project_id=None):
		return self._list(project_id)
	_list = abc.abstractmethod(lambda x: None)

@six.add_metaclass(abc.ABCMeta)
class CfgNotify(ControllerBase):

	def list(self, result_dict, project_id=None):
		return self._list(result_dict, project_id)
	_list = abc.abstractmethod(lambda x: None)

@six.add_metaclass(abc.ABCMeta)
class Mansync(ControllerBase):

	def sync(self, conf):
		return self._sync(conf)
	_sync = abc.abstractmethod(lambda x: None)

@six.add_metaclass(abc.ABCMeta)
class DriverBase(object):

	def __init__(self, conf):
		self.conf = conf
	
@six.add_metaclass(abc.ABCMeta)
class ControlDriverBase(DriverBase):

	@abc.abstractproperty
	def user_controller(self):
		raise NotImplementedError

	@abc.abstractproperty
	def business_controller(self):
		raise NotImplementedError
	
	@abc.abstractproperty
	def cfg_notify_controller(self):
		raise NotImplementedError

	@abc.abstractproperty
	def mansync_controller(self):
		raise NotImplementedError
