#echo function
def echo(self, args):
    out = ''
    for word in args:
        out += word+' '
    print(out)
#function reference, min args, max args, help info, case sensitive?, function name
func_alias = 'echo'
func_info = (echo,
             0,
             1,
             'Prints all arguments back to the user.',
             False,
             )

