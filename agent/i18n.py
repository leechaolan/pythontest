"""oslo.i18n integration module"""

import oslo_i18n as i18n

_translators = i18n.TranslatorFactory(domain='nmc_agent')

_ = _translators.primary
