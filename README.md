# CLI Generator

Generate intuitive CLI frontends/tools from your Python module or function.

**License:** MIT

## Usage

CLI Generator is implemented as a class, `CLIGenerator`.

To use, simply pass a function or module object to a new instance
(like: `gen = CLIGenerator(my_function_or_module)`), then you can get the code through `generate()` (like: `print(gen.generate())`).

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
$ python3 test_prog.py --num-b 7
12

$ python3 test_prog.py --num-b 7
test_prog.py: error: the following arguments are required: num_a

$ python3 test_prog.py 5
8

$ python3 test_prog.py --help
usage: test_prog.py command options

A CLI tool for my_function

positional arguments:
  command     Command to run.

optional arguments:
  -h, --help
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

$ python3 test_prog.py --hello 'Bye' --world 'everyone!'
Bye, everyone!

$ python3 test_prog.py tab 'Hello'
	Hello

$ python3 test_prog.py detab '	Hello'
Hello
```
