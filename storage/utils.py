import time
import httplib2
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
	#set request timeout=15 to avoid block.
	http = httplib2.Http(timeout=15)
	timestamp = int(time.time())
	try:
		resp, context = http.request(url,
				                     method="POST",
									 headers={'Context-Type': 'application/x-www-form-urlencoded'},
									 body=urllib.urlencode(req_body_dict))
	except (httplib2.HttpLib2Error, socket.error) as ex:
		LOG.error(u'Request time out %s', url)
		return False
	list_result = context.decode()
	return list_result
