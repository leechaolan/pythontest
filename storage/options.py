""" SQLalchemy storage driver implementation """

from oslo_config import cfg

_deprecated_group = 'drivers:storage:sqlalchemy'
_COMMON_SQLALCHEMY_OPTIONS = (
	cfg.StrOpt('uri', default='mysql+pymysql:///',
	           deprecated_opts=[cfg.DeprecatedOpt(
			                    'uri',
								group=_deprecated_group), ],
			   help='An sqlalchemy URL'),
)

MANAGEMENT_SQLALCHEMY_OPTIONS = _COMMON_SQLALCHEMY_OPTIONS
MANAGEMENT_SQLALCHEMY_GROUP = 'drivers:management_store:sqlalchemy'


def _config_options():
	return [(MANAGEMENT_SQLALCHEMY_GROUP, MANAGEMENT_SQLALCHEMY_OPTIONS)]
