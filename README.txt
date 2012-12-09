A modular console application: it dynamically loads properly formatted modules from the tools_functions directory. The name of the module is irrelevant, but it must be written to template.

Template for command modules:

max_args = <a number: max arguments passed to this function from the console; -1 means no max>
help_info = <a string: this determines what is printed for the function when user calls help>
case_sensitive = <a boolean: determines whether the arguments for this function are automatically made lowercase>
command_name = <a string: this is the name of the command, and MUST BE IDENTICAL to the name of the function defined below>
settings = <an OPTIONAL dict: this can be omitted, but it includes any settings needed to run the command>


def <command_name>(self,args):
	this is where the actual function goes; arguments come in as a list of strings in args[] and self contains a reference to the calling class. 