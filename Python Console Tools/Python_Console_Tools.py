import sys, os, importlib, inspect, string

#
# So, all of this looking for files needs to be done relative to the homeRoute and toolsRoute variables established here
# because if we leave it the way it is right now, these files are looked for in the directory you RUN IT FROM (see: console)
# instead of the directory it's in. Also, the address_book could probably use some polish, and we might want to drop
# zip module. And maybe a math module?
#

class ConsoleTools:
    #note that these are static; variables declared in a class and not as part of an __init__ belong to the class as a whole
    intro = 'Welcome to the tool console, just for tools. If you are confused, type "help".'
    prompt = '(Tools): '
    settingsWarning = '<Warning: do not edit this file. If you have problems, delete it and let the tool console create a new one>\n\nSettings:\n'
    stop = None
    homeRoute = os.path.split(os.path.realpath(__file__))[0]
    subDir = 'tools_functions'
    toolsRoute = os.path.join(homeRoute, subDir)

    #To add a setting, simply add its alias and default value (both must be strings) to the settings dict. Note the value will have to be interpreted later
    #Note the file check is not very sophisticated; if you adjust settings in code, it's best to just delete the file and let the application generate a new one
    def simpleEncrypt(self, item):
        encrypt = str.maketrans(string.ascii_lowercase+string.ascii_uppercase+string.digits, string.digits+string.ascii_uppercase+string.ascii_lowercase)
        return item.translate(encrypt)

    def simpleDecrypt(self, item):
        revert = str.maketrans(string.digits+string.ascii_uppercase+string.ascii_lowercase, string.ascii_lowercase+string.ascii_uppercase+string.digits)
        return item.translate(revert)

    def confirmationPrompt(self, prompt = "yes/no:"):
        while True:
            inp = input(prompt).lower()
            if inp == 'yes':
                return True
            elif inp == 'no':
                return False
            else:
                print('Error: input not recognized. Please enter "yes" or "no".')
    def boolSetting(self, setting):
        if self.settingsList[setting][0].lower() == 't':
            return True
        elif self.settingsList[setting][0].lower() == 'f':
            return False
        else:
            raise TypeError("Setting was not any of 'T', 'F', 't', 'f'")


    settingsList = {}
    def write_settings(self):
            sFile = open('settings.tool', 'w')
            sFile.write(self.settingsWarning)
            for key in self.settingsList:
                sFile.write(key+' - '+self.settingsList[key][0]+'\n')
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
                    self.settingsList[key] = (temp, self.settingsList[key][1])
            sFile.close()
        else:
            print('settins.tool file not found. Generating a settings file with default settings.\n')
        self.write_settings()

    def init_functions(self):
        if not os.path.isdir(self.toolsRoute):
            print('tools_functions directory not found. Empty directory will be created.\n')
            os.mkdir(self.toolsRoute)
            return;
        sys.path.insert(0,self.toolsRoute)
        importList = os.listdir(self.toolsRoute)
        for imp in importList:
            if (imp[-3:]) == '.py':
                module = imp[:-3]
                obj = importlib.__import__(module) #this line causes mac specific problems
                #possibilities include a difference in filenames (I'm pulling out '.py'), directory structure (I don't think so)
                #or the fact that I'm explicitly doing an importlib.__import__ but thsi also shouldn't matter
                #also, possibly a redundant import of the address book, although I'm not sure
                try:
                    self.functions[getattr(obj, 'func_alias')] = getattr(obj, 'func_info')
                    settings = getattr(obj, 'settings', False)
                    if settings:
                        for key in settings:
                            self.settingsList[key] = settings[key]
                except AttributeError:
                    print('Failed to load ' + imp + ' because it is not a properly formatted tools\nmodule. Please ensure it is written to template (check the readme).')
                 #When writing modules for this program, command_name should be the same as the name of the function that will be called within the module

    #Important: this is where functions are defined, before being listed in the dict. All available tool functions must take (self, args)

    def quit(self, args):
        print('Quitting...')
        self.stop = True

    def help(self, args):
        for key in self.functions:
            print(key+': '+self.functions[key][3]+'\n')

    def settings(self, args):
        for key in self.settingsList:
            if self.settingsList[key][1]:
                print(key+': <encrypted>')
            else:
                print(key+': '+self.settingsList[key][0])

    def set(self, args):
        if args[0] in self.settingsList:
            if self.settingsList[args[0]][1]:
                self.settingsList[args[0]] = (self.simpleEncrypt(args[1]), self.settingsList[args[0]][1])
            else:
                self.settingsList[args[0]] = (args[1], self.settingsList[args[0]][1])
            self.write_settings()
        else:
            print("Error: Invalid setting.")




    #Important: this is the function dict. It holds functions as tuples in the form function_name: (function, min_args, max_args, help info). -1 means no max
    functions = {'help':(help, 0, 0, 'Lists commands and their effects.', False),
                 'settings':(settings, 0, 0, 'Lists current settings.', False),
                 'set':(set, 2, 2, 'set: <setting> <value> sets the given setting to the given value.', True),
                 'exit':(quit, 0, 0, 'Quits the program.', False),
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
        max = self.functions[cmd][2]
        min = self.functions[cmd][1]
        length = len(args)
        if length < min:
            print('Error: %s takes at minimum %s arguments. Command cannot be executed.' % (cmd, max,))
            return
        elif max != -1 and length > max: #-1 check comes first because Python does support short-circuiting for 'and' and 'or'
            print('Error: %s takes up to %s arguments. The last %s arguments will be discarded.' % (cmd, max, length-max))
            while len(args) > max:
                args.pop()
        self.functions[cmd][0](self, args)


    def mainloop(self):
        self.init_functions()
        self.init_settings()
        print(self.intro)
        while not self.stop:
        #It saves the args in lower case and Raw form, then decides which to use based on the command.
        #this is general: if we decide that any other command requires case-sensitive input, we can just change its case_sensitive variable
            parsed = self.parseline(input(self.prompt))
            cmd = parsed[0]
            if cmd in self.functions:
                if self.functions[cmd][4]:
                    args = parsed[2]
                else:
                    args = parsed[1]
                self.callfunc(cmd, args)
            else:
                print('Error: Unrecognized command. Type "help" for a list of commands.')



ConsoleTools().mainloop()
