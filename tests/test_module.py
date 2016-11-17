from context import cligenerator
import subprocess as sp
import mymodule
import sys

def test_create_cli():

	print('\nCreating CLI for mymodule ({}).'.format(mymodule.__file__))

	cligen = cligenerator.CLIGenerator(mymodule)

	with open('cli_module.py', 'w') as f:
		f.write(cligen.generate())

def test_cli_greet():

	actual = sp.check_output([sys.executable, 'cli_module.py', 'greet'], universal_newlines=True)
	assert actual.rstrip() == 'Hello, World!'

	actual = sp.check_output([sys.executable, 'cli_module.py', 'greet', '--hello', 'Bye'], universal_newlines=True)
	assert actual.rstrip() == 'Bye, World!'

	actual = sp.check_output([sys.executable, 'cli_module.py', 'greet', '--hello', 'Bye', '--world', 'everyone!'],
			universal_newlines=True)
	assert actual.rstrip() == 'Bye, everyone!'

def test_cli_tab():

	actual = sp.check_output([sys.executable, 'cli_module.py', 'tab', 'Hello'], universal_newlines=True)
	assert actual.rstrip() == '\tHello'

def test_cli_untab():

	actual = sp.check_output([sys.executable, 'cli_module.py', 'untab', '	Hello'], universal_newlines=True)
	assert actual.rstrip() == 'Hello'

