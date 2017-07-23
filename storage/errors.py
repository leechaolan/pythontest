

class ExceptionBase(Exception):

	msg_format = ''

	def __init__(self, **kwargs):
		msg = self.msg_format.format(**kwargs)
		super(ExceptionBase, self).__init__(msg)

