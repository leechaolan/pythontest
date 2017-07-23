import sqlalchemy as sa
from oslo_db.sqlalchemy import engines
from storage import controller as con
import storage
from storage import options

class ControlDriver(storage.ControlDriverBase):

	def __init__(self, conf):
		super(ControlDriver, self).__init__(conf)
		self.conf.register_opts(options.MANAGEMENT_SQLALCHEMY_OPTIONS,
				                group=options.MANAGEMENT_SQLALCHEMY_GROUP)
		self.sqlalchemy_conf = self.conf[options.MANAGEMENT_SQLALCHEMY_GROUP]
		self.engine = self.engine()

	def _mysql_on_connect(self, conn, record):
		# This is necessary in order to 
		# ensure that all date operations im mysql
		# happened in UTC 
		conn.query('SET time_zone = "+0:00"')

	def engine(self):
		uri = self.sqlalchemy_conf.uri
		engine = engines.create_engine(uri, sqlite_fk=True)
	
		if (uri.startswith('mysql://') or
		        uri.startswith('mysql+pymysql://')):
				# oslo_db.create_engine makes a test connection, throw that out first
				# mysql time_zone can be added to oslo_db as a startup option
				engine.dispose()
				sa.event.listen(engine, 'connect', 
						        self._mysql_on_connect)
		
		return engine
	
	def run(self, *args, **kwargs):
		return self.engine.execute(*args, **kwargs)

	def close(self):
		pass

	@property
	def user_controller(self):
		controller = con.UserController(self)
		return controller

	@property
	def business_controller(self):
		controller = con.BusinessController(self)
		return controller
