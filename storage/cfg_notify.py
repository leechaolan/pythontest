from oslo_log import log
import sqlalchemy as sa
import storage
from storage import tables
from storage import utils

LOG = log.getLogger(__name__)

class CfgNotifyController(storage.CfgNotify):

	def _list(self, project_id=None):
		pass
