import functools
from oslo_log import log as logging
import i18n as _

LOG = logging.getLogger(__name__)

def on_exception_send_500(func):

	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except Exception as ex:
			LOG.exception(ex)
			error = _("Unexcepted error.")
			headers = {'status', 500}
			req = args[1]
			return error_response(req, ex, headers, error)

	return wrapper

def error_response(req, exception, headers=None, error=None):
	body = {'exception': str(exception), 'error': error}
	resp = response.Response(req, body, headers)
	return resp
