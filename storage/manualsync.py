from oslo_log import log
import sqlalchemy as sa
import storage
from storage import tables
from storage import utils
import service

LOG = log.getLogger(__name__)

class MansyncController(storage.Mansync):

	def _sync(self, conf):
		periodic_task = service.Periodic_Task(conf, self.driver)
		periodic_task.list_boss_pe_endpointt()
		periodic_task.format_pe_list_result()
		periodic_task.pe_contrast_to_local_db()
		periodic_task.list_boss_ce_endpoint()
		periodic_task.format_ce_list_result()
		periodic_task.ce_contrast_to_local_db()
