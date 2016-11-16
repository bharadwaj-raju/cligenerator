# CLI Generator

Generate intuitive CLI frontends/tools from your Python module or function.

**License:** MIT

## Installation

Use `pip`!

    $ pip install cligenerator

## Usage

CLI Generator is implemented as a class, `CLIGenerator`.

To use, simply pass a function or module object to a new instance
(like: `gen = cligenerator.CLIGenerator(my_function_or_module)`), then you can get the code through `generate()` (like: `print(gen.generate())`).

## Examples

### From function

Let's make a CLI for a function that adds two numbers.

```python
import cligenerator

def my_function(num_a, num_b=3):
	return int(num_a) + int(num_b)

cligen = cligenerator.CLIGenerator(my_function)

# Save our CLI to a file
with open('test_prog.py', 'w') as test_prog_file:
	test_prog_file.write(cligen.generate())
```

Now our CLI program is in `test_prog.py`.

**Running the CLI:**

```bash
$ python3 test_prog.py
usage: test_prog.py [-h] [--num-b NUM_B] num_a
test_prog.py: error: the following arguments are required: num_a

$ python3 test_prog.py --help
usage: test_prog.py [-h] [--num-b NUM_B] num_a

A CLI tool for my_function

positional arguments:
  num_a

optional arguments:
  -h, --help     show this help message and exit
  --num-b NUM_B

$ python3 test_prog.py 5
8

$ python3 test_prog.py 5 --num-b 2
7

$ python3 test_prog.py 10 --num-b 4
14
```

### From module

Let's make a CLI for a simple module.

`mymodule.py`:

```python
# A simple module

def greet(hello='Hello', world='World!'):
	return hello + ', ' + world

def tab(text):
	return '\t' + text

def untab(text):
	return tab.lstrip('\\t').lstrip()
```

**Making the CLI:**

```python
import mymodule
import cligenerator

cligen = cligenerator.generate()

with open('test_prog.py', 'w') as test_prog_file:
	test_prog_file.write(cligen.generate())
```

**Running the CLI:**

```bash
$ python3 test_prog.py
usage: test_prog.py command options
test_prog.py: error: the following arguments are required: command

$ python3 test_prog.py greet
Hello, World!

$ python3 test_prog.py greet --world 'everyone!'
Hello, everyone!

$ python3 test_prog.py greet --hello 'Bye' --world 'everyone!'
Bye, everyone!

$ python3 test_prog.py tab 'Hello'
	Hello

$ python3 test_prog.py detab '	Hello'
Hello
```

## Documentation

### Options

| Option               | Type       | Description                                                                                           |
|----------------------|------------|-------------------------------------------------------------------------------------------------------|
| `module_or_function` | `str`      | The module or function for which to generate a CLI for. **Required**                                  |
| `name`               | `str`      | The display name of the CLI tool generated.                                                           |
| `description`        | `str`      | The description of the CLI tool (to be displayed in the tool)                                         |
| `library_name`       | `str`      | The library name to be displayed in the CLI tool.                                                     |
| `help_strings`       | `dict`     | The strings to be displayed in `--help` etc. See [Help Strings](#help-strings)                        |
| `option_types`       | `dict`     | The type for each option. See [Option Types](#option-types).                                          |
| `ignore_modules`     | `list`     | Ignore the specified modules when looking for submodules.                                             |
| `ignore_functions`   | `list`     | Ignore the specified functions.                                                                       |
| `recurse_modules`    | `bool`     | Whether or not to recurse looking for modules. See [Recurse Modules](#recurse-modules).               |
| `additional_imports` | `list`     | Additional modules to import in the generated CLI.                                                    |

All these options are passed at initialization time (i.e. when assigning to `CLIGenerator()`).

### How it works

All the code is implemented in the class `CLIGenerator()`.

#### Functions

`CLIGenerator()` uses Python's introspection to get the arguments of the function (implemented in the internal function `_get_arguments(func)`), then it simply formats them into an `argparse` template.

#### Modules

`CLIGenerator()` simply lists functions in an object (and if recursing is enabled through the [option](#options) `recurse_modules`, sub-modules too), then applies the [function](#functions) method on each.

### Help Strings

(See the entry in [Options](#options).)

Help strings is the dictionary where `CLIGenerator()` looks for option help and function (i.e. command) descriptions.

If not given here, function (i.e. command) descriptions are taken from the first line of the function's docstring (if it exists, otherwise left blank).

**Format:**

You can nest it so:

- module → function : description
- module → function → option : help
- function → option : help
- function : description

(Where 'help' and 'description' are `str`s with the help/description content for that option/function)

### Option Types

(See the entry in [Options](#options))

Option types is the dictionary where `CLIGenerator()` looks for option types, since it *mostly* cannot autodetect them.

If not given here, option types are either detected from their default value (if specified, otherwise left to the default of `str`).

**Format:**

You can nest it so:

- module → function → option : type
- function → option : type
- option : type

(Where 'type' is a `class` of a type, like `int`, `str`, etc. *NOTE:* It is like `int`, *not* like `'int'` (i.e. *not* the class name in a `str`))

### Recurse Modules

(See the entry in [Options](#options))

*NOTE:* This is only applicable when generating for a module.

When looking for functions to generate the CLI with (see [How it Works: Modules](#modules)), by default, up to 1 sub-modules are also taken in.

You can make it multi-level by using this option (`recurse_modules`).

### Methods

Of the methods that can be called on the class, only `generate()` is important and useful.

The rest (all prefixed by an underscore `_`) are internal implementation details.

### Changes to option names

To make the CLI intuitive and standard, option names are modified a bit:

- Underscores are replaced with dashes (`-`).
- If an option's name *ends* with an underscore, that underscore is removed.

Your function or module doesn't have to worry about any of this.

