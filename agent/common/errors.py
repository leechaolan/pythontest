class InvalidDriver(Exception):
	""" A driver was not found or loaded. """

class PatternNotFound(Exception):
	""" A string did not match the excepted pattern or regex. """

class InvaliedAction(Exception):
	""" Raised when attempted a non existent action """

class ConfigurationError(Exception):
	""" An invalid value was used for a nmc_agent configuration option. """
