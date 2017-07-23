from oslo_config import cfg

_GENERAL_OPTIONS = (
	cfg.IntOpt('periodic_task_interval', default=60*60*24,
		       help='The period task interval default 3600 second'),
)

_DRIVER_OPTIONS = (
	cfg.StrOpt('transport', default='wsgi', 
		       help='Transport driver to use.'),	
)

_DRIVER_GROUP = 'drivers'

def _config_options():
	return [(None, _GENERAL_OPTIONS),
	        (_DRIVER_GROUP, _DRIVER_OPTIONS)]
