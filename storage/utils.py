import time
import httplib2
import httplib
import urllib
import socket
import json
from stevedore import driver
from oslo_serialization import jsonutils
from oslo_log import log
from common import errors
import hashlib

LOG = log.getLogger(__name__)

def load_storage_driver(conf, storage_type, control_mode, control_driver):
	mod = 'control'
	driver_type = 'pythontest.{0}.storage'.format(mod)
	_invoke_args = [conf]
#if control_driver is not None:
#_invoke_args.append(control_driver)

	try:
		mgr = driver.DriverManager(driver_type,
				                   'sqlalchemy',
								   invoke_on_load=True,
								   invoke_args=_invoke_args)
		return mgr.driver
	
	except Exception as exc:
		LOG.error('Failed to load "{}" driver for "{}"'.format(
			driver_type, storage_type))
		LOG.exception(exc)
		raise errors.InvalidDriver(exc)

def json_decode(binary):
	jsonutils.loads(binary, 'utf-8')

def to_json(obj):
	return json.dumps(obj, ensure_ascii=False)

def md5sum(code_str):
	hashmd5 = hashlib.md5()
	hashmd5.update(code_str)
	return hashmd5.hexdigest()

def make_notify(req_body_dict, url):
	http = httplib2.Http(".cache", timeout=10)

	#http.force_exception_to_status_code = True
	try:
		resp, context = http.request(url,
				                     method="POST",
									 headers={'Context-Type': 'application/x-www-form-urlencoded'},
									 body=jsonutils.dumps(req_body_dict))
	except httplib2.HTTPConnectionWithTimeout:
		LOG.error(u'Connect to %(url)s timeout.', 
				  {'url': url})
		print(u'Connect to %(url)s timeout.', 
				  {'url': url})
		return {}
	except socket.timeout:
		LOG.error(u'Connect to %(url)s TIMEOUT',
				  {'url': url})
		print(u'Connect to %(url)s TIMEOUT',
				  {'url': url})
		return {}
	except httplib.ResponseNotReady:
		LOG.error(u'Response not ready. Retry later.')
		return {}
	if resp.status is not 200:
		LOG.error(u'POST %s %s HTTP:%s', url, context, resp.status)
		return {}

	try:
		list_result = context.decode()
	except httplib2.FailedToDecompressContent, e:
		return {}

	return list_result
