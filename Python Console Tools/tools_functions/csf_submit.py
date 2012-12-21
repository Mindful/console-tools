#-----------------
#It is important to note that this module does not actually perform any file operations; it wraps pscp and plink. Along those lines,
#pscp.exe and plink.exe must both be in the same directory as the module (tools_functions) in order for it to work properly.


#WRITE A FUNCTION SPECIFICALLY FOR VIEWING
#-----------------
import os, inspect, subprocess, sys, time

from queue import Queue, Empty
from threading import Thread

class adaError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class outReader:
    
    def __init__(self, outStream, toPrint = False, ignoreString = None):
        self.ignoreString = ignoreString
        self.q = Queue()
        self.printNext = False
        self.dead = False
        self.t = Thread(target=self.enqueue_output, args=(outStream, self.q))
        self.t.daemon = True
        self.t.start()
        self.display = toPrint

    def enqueue_output(self, outStream, queue):
        for line in iter(outStream.readline, b''):
            if self.dead:
                return
            queue.put(line)
            line = line.decode()
            if self.display and (not self.ignoreString or line.find(self.ignoreString) == -1):
                sys.stdout.write(line)
            elif self.printNext:
                print(line)
                self.printNext = False

subjects = ['discretemath', 'java', 'arch', 'probsolv']
def submit(self, args):
    #All these if(x) then return statements are just error checking. want to make sure everything's in order before we try an upload
    pscproute = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],'pscp.exe')))
    plinkroute = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],'plink.exe')))
    if not (os.path.exists(pscproute)):
        print('Error: could not find pscp.exe in the tools_functions directory.')
        return
    if not (os.path.exists(plinkroute)):
        print('Error: could not find plink.exe in the tools_functions directory.')
        return
    usName = self.simpleDecrypt(self.settingsList['ada_username'][0])
    if len(args) < 2:
        if args[0].lower() == 'view': #the .lower here will be redundant if we find this function not to be case sensitive
            print('\nViewing files for ' +usName+'...')
            try:
                view_ada(self, usName)
            except adaError as err:
                print("Error interfacing with Ada: "+err.value)
            else:
                print('Success!')
        else:
            print("Error: insufficient arguments.")
        return
    if args[0] not in subjects:
        toPrint = 'Error: invalid subject.\nValid subjects are:'
        for subj in subjects:
            toPrint+=' ' +subj
        print(toPrint)
        return
    if not (os.path.exists(args[1])):  #right now there's really no good way to get filenames with spaces; will have to come back to this
        print('Error: could not find file. Remember that files are searched for relative to the tools console.')
        return
    #THIS is where we check if the file is a directory, and then we zip it, otherwise we check if it's a pdf and if it's not we spaz out
    fileName = args[1] #may sometimes be exactly args[1], but othertimes it will be zipped folder
    print('\nUploading ' + fileName + '...')
    try:
        upload_ada(self, fileName, usName)
    except adaError as err:
        print("Error interacting with Ada: "+err.value)
        return
    #catch exceptions from failure of upload
    print('Preparing to submit as ' +usName+'...')
    try:
        submit_ada(self, args[0], fileName, usName)
    except adaError as err:
        print("Error interfacing with Ada: "+err.value)
    else:
        print('Success!')

    

def upload_ada(self, file, user):
    uploadArgs = [self.toolsRoute+'\\'+'pscp.exe', 
                  '-pw', 
                  self.simpleDecrypt(self.settingsList['ada_password'][0]),
                  file,
                  user+'@ada.evergreen.edu:/home/'+user,
                  ]
    proc = subprocess.Popen(uploadArgs, bufsize=1, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        s = proc.communicate(None, 15)[0].decode("utf-8")
    except subprocess.TimeoutExpired as err:
        proc.kill()
        raise adaError("process timed out.")
        return
    if s.rfind(file)!= -1:
        print(s)
    else:
        raise adaError(s)

def view_ada(self, user):
    connectionArgs = [self.toolsRoute+'\\'+'plink.exe', 
                  '-ssh', 
                  '-pw', 
                  self.simpleDecrypt(self.settingsList['ada_password'][0]),
                  user+'@ada.evergreen.edu',
                  ]
    serverCommands = ("csf_submit view", "exit")
    discardString = ']0;'+user+'@ada: ~[0;32m'+user+'[0;37m@[0;32mada[00m:[01;34m~[00m$ '
    proc = subprocess.Popen(connectionArgs, bufsize=1, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    reader = outReader(proc.stdout, ignoreString = discardString)
    counter = 0
    while True:
        try:
            line = reader.q.get_nowait()
        except Empty:
            time.sleep(0.5)
            counter = counter + 1
            if counter > 25:
                proc.kill()
                raise adaError("process could not complete.")
                return
        else:
            line = line.decode()
            if line.find("Last login:") == 0:
                print("-->login")
                print(line)
                print("-->"+serverCommands[0])
                proc.stdin.write(formatCmd(serverCommands[0]))
                proc.stdin.flush()
                reader.display = True
            elif line.find(serverCommands[0]) != -1:
                break
    reader.dead = True
    try:
        proc.communicate(formatCmd(serverCommands[1]), 15)
    except subprocess.TimeoutExpired as err:
        proc.kill()
        raise adaError("process timed out.")
        return


def submit_ada(self, thread, file, user):
    overwrite = (self.settingsList['csf_overwrite'][0].lower() != 'f') # need a better convention for getting from string to bool
    connectionArgs = [self.toolsRoute+'\\'+'plink.exe', 
                  '-ssh', 
                  '-pw', 
                  self.simpleDecrypt(self.settingsList['ada_password'][0]),
                  user+'@ada.evergreen.edu',
                  ]
    if overwrite:
        serverCommands = ("csf_submit "+thread+" "+file, "exit", "yes")
    else:
        serverCommands = ("csf_submit "+thread+" "+file, "exit", "no")
    discardString = ']0;'+user+'@ada: ~[0;32m'+user+'[0;37m@[0;32mada[00m:[01;34m~[00m$ '
    proc = subprocess.Popen(connectionArgs, bufsize=1, shell=False, stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    reader = outReader(proc.stdout)
    counter = 0
    while True:
        try:
            line = reader.q.get_nowait()
        except Empty:
            time.sleep(0.5)
            counter = counter + 1
            if counter > 25:
                proc.kill()
                raise adaError("process could not complete.")
                return
        else:
            line = line.decode()
            if line.find("Last login:") == 0:
                print("-->login")
                print(line)
                proc.stdin.write(formatCmd(serverCommands[0]))
                proc.stdin.flush()
            elif line.find(discardString + serverCommands[0]) != -1:
                print("-->"+serverCommands[0])
                reader.printNext = True
                proc.stdin.write(formatCmd(serverCommands[2])) #dependant on override settings
                proc.stdin.flush()
            elif line.find("cp: overwrite") != -1:
                if overwrite:
                    print("-->overwrote file on server")
                else:
                    print("-->file detected on server, did not overwrite")
            elif line.find("Assignment " + file + " for student " + user + " submitted.") != -1:
                print(line)
                break
    reader.dead = True
    try:
        proc.communicate(formatCmd(serverCommands[1]), 15)
    except subprocess.TimeoutExpired as err:
        proc.kill()
        raise adaError("process timed out.")
        return

def formatCmd(cmd):
    return (cmd+"\n").encode("utf-8")

func_alias = 'csf_submit'
func_info = (submit,
             1, 
             2, 
            'csf_submit <subject> <file> uploads the given file to Ada and submits it for the given subject. csf_submit view lists current assignments on csf_submit.',
            False, #may end up this does need to be case sensitive; we'll see
            )
settings = {'ada_username':('', True),'ada_password':('', True), 'csf_overwrite':('F', False)}

