# A simple module

def greet(hello='Hello', world='World!'):
	return hello + ', ' + world

def tab(text):
	return '\t' + text

def untab(text):
	return text.lstrip('\\t').lstrip()

