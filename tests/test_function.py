from context import cligenerator
import subprocess as sp
import mymodule
import sys
import inspect

def my_function(a, b=3):

	return int(a) + int(b)

def test_create_cli():

	print('\nCreating CLI for my_function.')
	print(inspect.getsource(my_function))

	cligen = cligenerator.CLIGenerator(my_function)

	with open('cli_func.py', 'w') as f:
		f.write(cligen.generate())

def test_cli():

	actual = sp.check_output([sys.executable, 'cli_func.py', '3'], universal_newlines=True)
	assert actual.rstrip() == '6'

	actual = sp.check_output([sys.executable, 'cli_func.py', '3', '--b', '5'], universal_newlines=True)
	assert actual.rstrip() == '8'

