from oslo_log import log as logging
from common.api import utils as api_utils
from storage import errors as storage_errors

LOG = logging.getLogger(__name__)


class Endpoints(object):

	def __init__(self, storage):
		self._user_controller = storage.user_controller

	@api_utils.on_exception_send_500
	def User_list(self, req):

		project_id = req._headers.get('X-Project-ID')

		LOG.debug(u'User list - project: %(project)s',
				  {'project': project_id})

		try:
			#kwargs = api_utils.get_headers()
			results = self._user_controller.list(
				project_id=project_id, **kwargs)
			users = list(next(results))
		except storage_errors.ExceptionBase as ex:
			LOG.exception(ex)
			error = 'User could not be listed.'
			headers = {'status': 503}
			return api_utils.error_response(req, ex, headers, error)

		body = {'users', users}
		headers = {'status': 200}

		return response.Response(req, body, headers)
