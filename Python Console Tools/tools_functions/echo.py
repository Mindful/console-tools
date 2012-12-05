#echo function

max_args = -1
help_info = 'Prints all arguments back to the user.'
case_sensitive = False

def echo(self, args):
    out = ''
    for word in args:
        out += word+' '
    print(out)