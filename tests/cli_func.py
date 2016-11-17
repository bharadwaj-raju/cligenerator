import argparse
import sys


def my_function(a, b=3):

	return int(a) + int(b)



def __my_functionCLI():

	parser = argparse.ArgumentParser(description='A CLI tool for my_function')

	parser.add_argument('a')
	parser.add_argument('--b', type=int, default=3)


	args = parser.parse_args()

	try:
		print(test_function.my_function(**vars(args)))
	except:
		print(my_function(**vars(args)))




if __name__ == '__main__':
	__my_functionCLI()
