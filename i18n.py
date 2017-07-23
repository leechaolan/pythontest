"""oslo.i18n integration module"""

import oslo_i18n as i18n

_translators = i18n.TranslatorFactory(domain='pythontest')

_ = _translators.primary
