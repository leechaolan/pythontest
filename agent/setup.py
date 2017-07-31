import setuptools

try:
	import mulitprocessing
except ImportError:
	pass

setuptools.setup(
	setup_requires=['pbr>=2.0.0'],
	pbr=True
)
