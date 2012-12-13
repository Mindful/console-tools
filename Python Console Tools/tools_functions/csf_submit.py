import os, inspect, subprocess

subjects = ['discretemath', 'java', 'arch', 'probsolv']
def submit(self, args):
    #All these if(x) then return statements are just error checking. want to make sure everything's in order before we try an upload
    pscproute = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],'pscp.exe')))
    puttyroute = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],'putty.exe')))
    if not (os.path.exists(pscproute)):
        print('Could not find pscp.exe in the tools_functions directory. Aborting csf_submit.')
        return
    if not (os.path.exists(puttyroute)):
        print('Could not find putty.exe in the tools_functions directory. Aborting csf_submit.')
        return
    if args[0] not in subjects:
        toPrint = 'Invalid subject. Valid subjects are:'
        for subj in subjects:
            toPrint+=' ' +subj
        print(toPrint)
        return
    if not (os.path.exists(args[1])):  #right now there's really no good way to get filenames with spaces; will have to come back to this
        print('Couldn\'t find file. Try sucking less?')
        return
    #THIS is where we check if the file is a directory, and then we zip it, otherwise we check if it's a pdf and if it's not we spaz out
    #actual attempted upload starts here
    usName = self.simpleDecrypt(self.settingsList['ada_username'][0])
    #can't just be pscp, has to be entire path to pscp
    uploadArgs = [self.toolsRoute+'\\'+'pscp.exe', 
                  '-pw', 
                  self.simpleDecrypt(self.settingsList['ada_password'][0]),
                  args[1],
                  usName+'@ada.evergreen.edu:/home/'+usName,
                  ]
    subprocess.Popen('echo a b', shell=True,)
    proc = subprocess.Popen(uploadArgs, bufsize=1, shell=True,)





func_alias = 'csf_submit'
func_info = (submit,
             2, 
             2, 
            'csf_submit <subject> <file> uploads the given file to Ada and submits it for the given subject. Note the file location is assumed relative to the location of the tools console.',
            False, #may end up this does need to be case sensitive; we'll see
            )
settings = {'ada_username':('', True),'ada_password':('', True)}