import argparse
import sys
import mymodule

class MymoduleCLI(object):

	def __init__(self):

		parser = argparse.ArgumentParser(
			description='A CLI tool for mymodule',
			formatter_class=argparse.RawTextHelpFormatter,
			usage='%(prog)s command options',
			allow_abbrev=False)

		parser.add_argument('command', help='Command to run.')

		args = parser.parse_args(sys.argv[1:2])  # Ignore options

		self._one_func_mode = False

		if not hasattr(self, args.command.replace('.', '_')):
			print('Unrecognized command!')
			sys.exit(1)

		getattr(self, args.command.replace('.', '_'))()


	def untab(self):
	
		parser = argparse.ArgumentParser(description='')
	
		parser.add_argument('text')
	
		if self._one_func_mode:
			args = parser.parse_args(sys.argv[1:])
	
		else:
			args = parser.parse_args(sys.argv[2:])
	
		print(mymodule.untab(**vars(args)))

	def tab(self):
	
		parser = argparse.ArgumentParser(description='')
	
		parser.add_argument('text')
	
		if self._one_func_mode:
			args = parser.parse_args(sys.argv[1:])
	
		else:
			args = parser.parse_args(sys.argv[2:])
	
		print(mymodule.tab(**vars(args)))

	def greet(self):
	
		parser = argparse.ArgumentParser(description='')
	
		parser.add_argument('--hello', type=str, default='Hello')
		parser.add_argument('--world', type=str, default='World!')
	
		if self._one_func_mode:
			args = parser.parse_args(sys.argv[1:])
	
		else:
			args = parser.parse_args(sys.argv[2:])
	
		print(mymodule.greet(**vars(args)))



if __name__ == '__main__':
	MymoduleCLI()
