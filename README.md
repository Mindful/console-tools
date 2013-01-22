Python Tool Console
=========
A simple project intended to help me and another Evergreen State College student learn Python fundamentals. Nothing exceptionally complicated here: the main .py file is a simple console shell that loads specific commands as modules from the tools_functions directory. If you are just learning Python and want to write something simple without having to worry about a console shell, the template for modules is at the bottom of the readme (although it's worth noting that Python provides a library for this: [cmd](http://docs.python.org/3.3/library/cmd.html "Python cmd library")).

Included command modules:


  - A csf_submit module

This is for Evergreen CS students who are sick of moving their homework to their server before submitting it. It wraps plink/pscp (both must be in the tools_functions directory for it to function properly) and handles logging in and submitting homework. It will even handle zipping if you give it a directory. Note that this module relies on storing a verly lightly obscured copy of your username/password as settings.

  - An email to SMS module

This module will take a person's phone number and carrier and allow you to, in effect, text them via the console. It actually takes advantage of the email-to-text that is supported by almost every phone provider. (need more from the author of this module)

  -  Several other minor modules.


Module Template
---------------
```python
def exampleFunc(self,args):
    pass #this is where the actual function goes; arguments come in as a list of strings in args[] and self contains a reference to the calling class.

func_alias = 'example_function'  #a string that represents the name by which your function is called as a command. cannot include whitespace characters
func_info = (exampleFunc, #the actual function itself
             1, #the minimum number of arguments the function can take. fewer than min args will cause the function not to run
             1, #the maximum number of arguments the function can take. excess arguments will be discarded
            'This is a demo function; it does nothing.', #the information displayed about this function when a user runs the "help" command
            False, #a bool determining whether or not the function's input arguments are checked for case
            )
 #It's very important to note that while you can do whatever you want inside the module, your function owns the main console for only as long as it runs. 
 #Additionally, the func_alias and func_info variables MUST be formatted properly for the main console to load your module.
```