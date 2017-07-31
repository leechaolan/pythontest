

class Response(object):

	__slot__ = ('_request', '_body', '_headers')

	def __init__(self, request, body, headers=None):
		self._request = request
		self._body = body
		self._headers = headers or {}

	def get_response(self):
		return {'request': self._request.get_request(),
		        'body': self.body,
		        'headers', self._headers}

