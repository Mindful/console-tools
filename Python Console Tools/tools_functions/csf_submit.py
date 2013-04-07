#-----------------
#It is important to note that this module does not actually perform any file operations; it wraps pscp and plink. Along those lines,
#pscp.exe and plink.exe must both be in the same directory as the module (tools_functions) in order for it to work properly.
#-----------------
import os, inspect, subprocess, sys, time, zipfile, shutil, tarfile

from queue import Queue, Empty
from threading import Thread

linux = None

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
                self.printNext = False
                if not self.ignoreString or line.find(self.ignoreString) == -1:
                    print(line)

subjects = ['discretemath', 'java', 'arch', 'probsolv']
def submit(self, args):
    #All these if(x) then return statements are just error checking. want to make sure everything's in order before we try an upload
    global linux
    linux = self.linux
    if linux:
        plinktest = subprocess.Popen(['plink', '-V'], stdout=subprocess.PIPE)
        pscptest = subprocess.Popen(['pscp', '-V'], stdout=subprocess.PIPE)
        if not pscptest.communicate()[0].decode().startswith('pscp:'):
            print('Error: could not verify putty-tools/pscp installation.')
            return
        if not plinktest.communicate()[0].decode().startswith('plink:'):
            print('Error: could not verify putty-tools/plink installation.')
            return
    else:
        pscproute = os.path.join(self.toolsRoute, 'pscp.exe')
        plinkroute = os.path.join(self.toolsRoute, 'plink.exe')
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
    #this is where we start looking at formatting the file to upload it
    folder = os.path.normpath(args[1])
    loc, fold = os.path.split(folder)
    if loc == "":
        loc=self.homeRoute
    if os.path.isfile(folder):
        invalid = not (folder[-4:] == '.pdf' or zipfile.is_zipfile(folder) or tarfile.is_tarfile(folder))
        if invalid and not self.confirmationPrompt("Not a .pdf, .zip or .tar file. Are you sure you want to upload? "):
            return #"and" is short circuited; confirmation prompt only called if file not a suggested type
        fileName = fold
    elif os.path.isdir(folder):
        if not self.confirmationPrompt("You have given a directory. Would you like to zip and upload it? "):
            return
        shutil.make_archive(fold,'zip',loc,fold)
        fileName = fold+".zip"
    else:
        print("Error: could not find given folder or directory.")
        return
    #this is where we upload the file
    print('\nUploading ' + fileName + '...')
    try:
        upload_ada(self, fileName, usName)
    except adaError as err:
        print("Error interacting with Ada: "+err.value)
        return
    #and here we go onto ada to issue submit commands and interact with the possible override prompt
    print('Preparing to submit as ' +usName+'...')
    fileName = os.path.split(fileName)[1] #removes any possible superflous location information
    try:
        submit_ada(self, args[0], fileName, usName)
    except adaError as err:
        print("Error interfacing with Ada: "+err.value)
    else:
        print('Success!')

    

def upload_ada(self, file, user):

    if linux:
        uploadArgs = ['pscp', 
                      '-pw', 
                      self.simpleDecrypt(self.settingsList['ada_password'][0]),
                      file,
                      user+'@ada.evergreen.edu:/home/'+user,
                      ]
    else:
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
    if s.rfind("ETA: 00:00:00 | 100%")!= -1:
        print(s)
    else:
        raise adaError(s)

def view_ada(self, user):

    if linux:
        connectionArgs = ['plink', 
                '-ssh', 
                '-pw', 
                self.simpleDecrypt(self.settingsList['ada_password'][0]),
                user+'@ada.evergreen.edu',
                ]
    else:
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
    time.sleep(0.5)
    reader.dead = True
    try:
        proc.communicate(formatCmd(serverCommands[1]), 15)
    except subprocess.TimeoutExpired as err:
        proc.kill()
        raise adaError("process timed out.")
        return


def submit_ada(self, thread, file, user):
    try:
        overwrite = self.boolSetting('csf_overwrite')
    except TypeError:
        raise adaError('csf_overwrite setting was not a recognizable\nboolean value. Pleaseset csf_overwrite to "T" or "F".')

    if linux:
        connectionArgs = ['plink', 
                '-ssh', 
                '-pw', 
                self.simpleDecrypt(self.settingsList['ada_password'][0]),
                user+'@ada.evergreen.edu',
                ]
    else:
        connectionArgs = [self.toolsRoute+'\\'+'plink.exe', 
                      '-ssh', 
                      '-pw', 
                      self.simpleDecrypt(self.settingsList['ada_password'][0]),
                      user+'@ada.evergreen.edu',
                      ]
    if overwrite:
        serverCommands = ("csf_submit "+thread+" "+file, "exit", "y")
    else:
        serverCommands = ("csf_submit "+thread+" "+file, "exit", "n")
    discardString = ']0;'+user+'@ada: ~[0;32m'+user+'[0;37m@[0;32mada[00m:[01;34m~[00m$ '
    proc = subprocess.Popen(connectionArgs, bufsize=1, shell=False, stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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

