from oslo_config import cfg

_GENERAL_OPTIONS = (
)

_DRIVER_OPTIONS = (
	cfg.StrOpt('transport', default='wsgi', 
		       help='Transport driver to use.'),	
)

_DRIVER_GROUP = 'drivers'

def _config_options():
	return [(None, _GENERAL_OPTIONS),
	        (_DRIVER_GROUP, _DRIVER_OPTIONS)]
