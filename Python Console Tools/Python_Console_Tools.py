import sys, os, importlib, inspect

class ConsoleTools:
    intro = 'Welcome to the tool console, just for tools. If you are confused, type "help"'
    prompt = '(Tools): '
    settingsWarning = '<Warning: do not edit this file. If you have problems, delete it and let the tool console create a new one>\n\nSettings:\n'
    stop = None

    #To add a setting, simply add its alias and default value (both must be strings) to the settings dict. Note the value will have to be interpreted later
    #Note the file check is not very sophisticated; if you adjust settings in code, it's best to just delete the file and let the application generate a new one
    settingsList = {}
    def write_settings(self):
            sFile = open('settings.tool', 'w')
            sFile.write(self.settingsWarning)
            for key in self.settingsList:
                sFile.write(key+' - '+self.settingsList[key]+'\n')
            sFile.close()

    def init_settings(self):
        if os.path.exists('settings.tool'):
            sFile = open('settings.tool', 'r+')
            for x in range (0, self.settingsWarning.count('\n')): 
                #This may look confusing, but in reality it's just discarding the warning before reading settings by reading lines and doing nothing with the data
                sFile.readline()
            tempList = sFile.read().splitlines()
            for item in tempList:
                temp = item[item.find('- '):].strip('- ')
                key = item[:item.find(' -')]
                if key in self.settingsList:
                    self.settingsList[key] = temp
            sFile.close()
        self.write_settings()

    def init_functions(self):
        subdir = 'tools_functions' #function directory
        route = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],subdir))) #MAGIC
        sys.path.insert(0,route)
        importList = os.listdir(subdir)
        for imp in importList:
            if (imp[-3:]) == '.py':
                module = imp[:-3]
                obj = importlib.__import__(module)
                self.functions[getattr(obj, 'command_name')] = (getattr(obj, module), getattr(obj, 'max_args'), getattr(obj, 'help_info'), getattr(obj, 'case_sensitive'))
                settings = getattr(obj, 'settings', False)
                if settings:
                    for key in settings:
                        self.settingsList[key] = settings[key]
                 #When writing modules for this program, command_name should be the same as the name of the function that will be called within the module

    #Important: this is where functions are defined, before being listed in the dict. All available tool functions must take (self, args)

    def quit(self, args):
        print('Quitting...')
        self.stop = True

    def help(self, args):
        for key in self.functions:
            print(key+': '+self.functions[key][2]+'\n')

    def settings(self, args):
        for key in self.settingsList:
            print(key+': '+self.settingsList[key])

    def set(self, args):
        if args[0] in self.settingsList:
            self.settingsList[args[0]] = args[1]
            self.write_settings()
        else:
            print("Error: Invalid setting.")




    #Important: this is the function dict. It holds functions as tuples in the form function_name: (function, max_args, help info). -1 means no max
    functions = {'help':(help, 0, 'Lists commands and their effects.', False),
                 'settings':(settings, 0, 'Lists current settings.', False),
                 'set':(set, 2, 'set: <setting> <value> sets the given setting to the given value', True),
                 'quit':(quit, 0, 'Quits the program.', False),
                 }


    def parseline(self,line):
        #Parses input, and then returns the (cmd, argsLower, argsRaw) as a tuple
        line = line.strip() 
        if not line:
            return None, None
        i = 0
        l = len(line)
        while i < l and line[i] != ' ': 
            i = i+1
        return line[:i].lower(), line[i:].lower().strip().split(), line[i:].strip().split()

    def callfunc(self, cmd, args):
        #Attempts to the call the function; handles extra args, and returns false if the function is invalid
        if cmd in self.functions:
            max = self.functions[cmd][1]
            length = len(args)
            if max != -1 and length > max: #-1 check comes first because Python does support short-circuiting for 'and' and 'or'
                print('Error: %s takes up to %s arguments. The last %s arguments will be discarded.' % (cmd, max, length-max))
                while len(args) > max:
                    args.pop()
            self.functions[cmd][0](self, args)
            return True
        else:
            return False

    def mainloop(self):
        self.init_functions()
        self.init_settings()
        print(self.intro)
        while not self.stop:
        #It saves the args in lower case and Raw form, then decides which to use based on the command.
        #this is general: if we decide that any other command requires case-sensitive input, we can just change its case_sensitive variable
            parsed = self.parseline(input(self.prompt))
            cmd = parsed[0]
            if self.functions[cmd][3]:
                args = parsed[2]
            if not self.functions[cmd][3]:
                args = parsed[1]
            if not self.callfunc(cmd, args):
                print('Error: Unrecognized command. Type "help" for a list of commands.')



ConsoleTools().mainloop()
