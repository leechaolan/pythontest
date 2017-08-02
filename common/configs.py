from oslo_config import cfg

_GENERAL_OPTIONS = (
	cfg.IntOpt('periodic_task_interval', default=60*60*24,
		       help='The period task interval default 3600 second'),
	cfg.StrOpt('boss_operate_config_url', default='http://0.0.0.0:9001/operation_config_query',
		       help='BOSS server operate LIST api'),
	cfg.StrOpt('boss_deploy_url', default='http://0.0.0.0:9001/business_deployment_notify',
		       help='BOSS server deploy notify api'),
	cfg.StrOpt('boss_business_config_url', default='http://0.0.0.0:9001/business_config_query',
		       help='BOSS server business LIST api'),
)

_DRIVER_OPTIONS = (
	cfg.StrOpt('transport', default='wsgi', 
		       help='Transport driver to use.'),	
)

_DRIVER_GROUP = 'drivers'

def _config_options():
	return [(None, _GENERAL_OPTIONS),
	        (_DRIVER_GROUP, _DRIVER_OPTIONS)]
