from distutils.core import setup
import subprocess as sp

version = '1.0.1'

setup(
	name='cligenerator',
	packages=['cligenerator'],
	version=version,
	description='Generate CLI tools from Python modules and functions',
	author='Bharadwaj Raju',
	author_email='bharadwaj.raju777@gmail.com',
	url='https://github.com/bharadwaj-raju/cligenerator',
	download_url='https://github.com/bharadwaj-raju/cligenerator/tarball/1.0.1',
	keywords = ['cli', 'argparse', 'interface', 'module', 'function', 'generate', 'command-line'],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Natural Language :: English",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.3",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: Implementation :: CPython",
		"Programming Language :: Python :: Implementation :: PyPy",
		"Topic :: Software Development :: Libraries :: Python Modules"
		]
	)
