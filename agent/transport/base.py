import abc
import six

def _config_options():
	return [
		(None, None),
	]

@six.add_metaclass(abc.ABCMeta)
class DriverBase(object):

	def __init__(self, conf):
		self._conf = conf
