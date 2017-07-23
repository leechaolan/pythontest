from api import endpoints

class Handler(object):

	def __init__(self, storage):
		self.endpoints = endpoints.Endpoints(storage)
