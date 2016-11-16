# coding: utf-8

# Licensed under the MIT license (see the LICENSE file or the text below)

# This file is part of cligenerator — generate CLI tools from Python libraries — also known as "CLI Generator" and "CLIGenerator" and "cli-generator"

# Copyright © 2016 Bharadwaj Raju

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import sys
import inspect
from textwrap import dedent


class CLIGenerator(object):

	def __init__(self, module_or_function, name='', description='', library_name='',
				help_strings={}, option_types={},
				ignore_modules=None, ignore_functions=None,
				recurse_modules=False,
				additional_imports=None):

		self.help_strings = help_strings
		self.option_types = option_types

		self.additional_imports = additional_imports or []

		self.module_or_function = module_or_function

		self.recurse_modules = recurse_modules

		self.name = name or self.module_or_function.__name__

		self.library_name = library_name or self.name

		self.description = description or 'A CLI tool for {}'.format(self.library_name)

		self.ignore_modules = ignore_modules or []
		self.ignore_functions = ignore_functions or []

		self.usage = '{name} [command] [options]'.format(name=name)

		if inspect.ismodule(module_or_function):
			self.mode = 'module'

		elif hasattr(module_or_function, '__call__'):
			self.mode = 'function'

		else:
			raise TypeError('module_or_function must be a valid module object or a function object!')

		# Base tool code
		# Code is built out of these by the generate* functions

		self.base_code = \
		dedent('''\
		import argparse
		import sys
		{additional_imports}

		class {class_name}(object):

			def __init__(self):

				parser = argparse.ArgumentParser(
					description='{description}',
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


		''').format(description=self.description,
					usage=self.usage,
					additional_imports='ADDITIONAL_IMPORTS',  # Don't replace now, since it'll be used again later
					class_name=self.name.capitalize().replace('-', '_').replace('.', '_') + 'CLI')

	def _object_tree(self, obj):

		tree = {}

		for i in dir(obj):
			obj_i = getattr(obj, i)

			if not i.startswith('_'):
				if hasattr(obj_i, '__call__') and obj_i.__name__ not in self.ignore_functions:
					tree[i] = obj_i

				elif inspect.ismodule(obj_i) and \
						obj_i.__name__.startswith(self.module_or_function.__name__) and \
						obj_i.__name__ not in self.ignore_modules:
					if self.recurse_modules:
						tree[i] = (obj_i, self.object_tree(obj_i))

					else:
						tree[i] = (obj_i, obj_i)

		return tree


	def _get_arguments(self, func):

		argc = func.__code__.co_argcount
		argv = func.__code__.co_varnames[:argc]

		argspec = inspect.getargspec(func)

		try:
			defaults = dict(zip(argspec.args[-len(argspec.defaults):], argspec.defaults))

		except TypeError:
			defaults = {}

		return (argv, defaults)


	def _get_option_type(self, func, option):

		def _type_to_str(type_):
			return repr(type_).replace('<class ', '').replace('>', '').replace("'", '').replace('Type', '')

		try:
			return _type_to_str(self.option_types[func.__module__][func.__name__][option])

		except KeyError:
			try:
				return _type_to_str(self.option_types[func.__name__][option])

			except KeyError:
				try:
					return _type_to_str(self.option_types[option])

				except KeyError:
					if option in self._get_arguments(func)[1]:
						return _type_to_str(type(self._get_arguments(func)[1][option]))

					else:
						return None

	def _get_function_description(self, func):

		try:
			return self.help_strings[func.__module__][func.__name__]

		except KeyError:
			try:
				return self.help_strings[func.__name__]

			except KeyError:
				if func.__doc__:
					return func.__doc__.splitlines()[0] or func.__doc__.splitlines[1]

				else:
					return ''

	def _get_option_help(self, func, option):

		try:
			return self.help_strings[func.__module__][func.__name__][option]

		except KeyError:
			try:
				return self.help_strings[func.__name__][option]

			except KeyError:
				try:
					return self.help_strings[option]

				except KeyError:
					return ''


	def _generate_function(self, func):

		func_name = '{}{}'.format(
				func.__module__ + '.' if func.__module__ != '__main__' else '',
				func.__name__
				)

		template = '''\
			def {name}(self):

				parser = argparse.ArgumentParser(description='{description}')

				{arg_defs}

				if self._one_func_mode:
					args = parser.parse_args(sys.argv[1:])

				else:
					args = parser.parse_args(sys.argv[2:])

				{function_call}
		'''

		arg_template = '''parser.add_argument('{arg_name}'{additional_opts})'''

		arg_defs = []

		func_args, func_defaults = self._get_arguments(func)

		for i in func_args:
			required = bool(i not in func_defaults)

			option_type = self._get_option_type(func, i)

			additional_opts = ''

			if option_type is not None and option_type != 'bool':
				additional_opts += ', type={}'.format(
						option_type if option_type != 'dict' else 'json.loads')

			elif option_type == 'bool':
				additional_opts += ', action=\'store_true\''

			if option_type == 'list':
				additional_opts += ', nargs=\'*\''  # nargs=* is zero or more values

			if option_type == 'dict':
				self.additional_imports.append('json')

			if not required:
				additional_opts += ', default={}'.format(
						"'{}'".format(func_defaults[i]) if isinstance(func_defaults[i], str) else func_defaults[i])

			if i.endswith('_') and not required:
				additional_opts += ', dest=\'{}\''.format(i[:])
				i = i[:-1]

			if self._get_option_help(func, i):
				additional_opts += ', help=\'{}\''.format(self._get_option_help(func, i))

			arg_defs.append(arg_template.format(
				arg_name=i if required else '--{}'.format(i.replace('_', '-')),
				additional_opts=additional_opts))

		function_call = 'print({}(**vars(args)))'.format(func_name)

		fmt_func_name = ''.join(func_name.split('.', 1)[1:]) or func_name

		self._name = fmt_func_name.replace('.', '_')[:]


		return dedent(template.format(
				name=fmt_func_name.replace('.', '_'),
				description=self._get_function_description(func),
				arg_defs='\n\t\t\t\t'.join(arg_defs) or '',
				function_call=function_call))


	def generate(self):

		global code
		code = self.base_code[:]

		if self.mode == 'module':
			self.additional_imports.append(self.module_or_function.__name__.split('.')[0])

			for i in self.additional_imports:
				self.additional_imports[self.additional_imports.index(i)] = 'import {}'.format(i) if not i.startswith('import ') else i

			code = code.replace('ADDITIONAL_IMPORTS', '\n'.join(self.additional_imports))

			module_tree = self._object_tree(self.module_or_function)


			def _recurse_code_update(tree):
				global code

				for i in tree:
					if isinstance(tree[i], tuple):
						# Module in module
						if self.recurse_modules:
							_recurse_code_update(tree[i][1])

					else:
						function_code = self._generate_function(tree[i]).splitlines()
						function_code[0] = '\t' + function_code[0]
						code += '\n\t'.join(function_code)

						code += '\n\n'

			_recurse_code_update(module_tree)

			call_obj = self.name.capitalize.replace('-', '_').replace('.', '_') + 'CLI'


		else:
			if hasattr(sys, 'ps1'):
				# Running interactively
				try:
					# dill works in interactive mode, inspect.getsource() doesn't
					import dill
					func_code = dill.source.getsource(self.module_or_function)

				except ImportError:
					try:
						func_code = inspect.getsource(self.module_or_function)

					except OSError:
						func_code = ''

			else:
				func_code = inspect.getsource(self.module_or_function)

			code = code.replace('ADDITIONAL_IMPORTS', '\n' + '\n'.join(self.additional_imports) + '\n' + func_code + '\n')

			function_code = dedent(self._generate_function(self.module_or_function))

			function_code = function_code.replace('def {}(self)'.format(self._name), 'def {}()'.format('__' + self._name + 'CLI'))

			function_code = function_code.replace('argparse.ArgumentParser(description=\'\')',
					'argparse.ArgumentParser(description=\'{}\')'.format(self.description))  # Won't do anything if specified already

			code = code.split('class {}(object)'.format(self.name.capitalize().replace('-', '_').replace('.', '_') + 'CLI'), 1)[0]

			to_remove = '''\tif self._one_func_mode:\n\t\targs = parser.parse_args(sys.argv[1:])\n\n\telse:\n\t\targs = parser.parse_args(sys.argv[2:])'''

			code += function_code

			code = code.replace(to_remove, '\n\targs = parser.parse_args()')

			code += '\n\n'

			call_obj = '__' + self._name + 'CLI'

		code += dedent('''

		if __name__ == '__main__':
			{}()
		'''.format(call_obj))

		return code

