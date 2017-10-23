import libvirt
from oslo_log import log

LOG = log.getLogger(__name__)

def start_domain(domain_name):
	conn = libvirt.open('qemu:///system')
	if conn == None:
		LOG.error(u'Failed to open connection to qemu:///system')
		return False

	domName = domain_name
	dom = conn.lookupByName(domName)
	if dom is None:
		LOG.error(u'Failed to fined the domain %s', domName)
		return False
	
	flag = dom.isActive()
	if flag == True:
		LOG.debug(u'domain %s is already running', domName)
	else:
		dom.create()
			
	conn.close()
	return True
