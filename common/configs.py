from oslo_config import cfg

_DRIVER_OPTIONS = (
	cfg.StrOpt('transport', default='wsgi', 
		       help='Transport driver to use.'),	
)

_DRIVER_GROUP = 'drivers'

def _config_options():
	return [(_DRIVER_GROUP, _DRIVER_OPTIONS)
		
	]
