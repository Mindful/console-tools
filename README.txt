A modular console application: it dynamically loads properly formatted modules from the tools_functions directory. The name of the module is irrelevant, but it must be written to template.

Template for command modules:

def <function>(self,args):
	this is where the actual function goes; arguments come in as a list of strings in args[] and self contains a reference to the calling class.

func_alias = 'name'  - a string that determines the name the function uses in the console
func_info = (<function reference>, - the actual function itself
             <min args>, - the minimum number of arguments the function can take. fewer than min args will cause the function not to run
             <max args>, - the maximum number of arguments the function can take. excess arguments will be discarded
            'help info', - the information displayed about this function when a user runs the "help" command
            <case sensitive?>, - a bool determining whether or not the function's input arguments are checked for case
            )
 