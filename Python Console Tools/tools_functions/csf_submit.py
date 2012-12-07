# zip_submit
# NOTES:
# at this point, the module is fine for zipping up directories.
# Plans:
# - prevent unnecessary subdirectories in the end .zip folder
#    currently the program will recreate the entire supplied path within the .zip, including directories who's only content is a single directory
#    this is unecessary and makes me feel bad about submitting the .zip on ada
# - add the ssh and submit portions...

import sys, os, zipfile
from os import path

max_args = 2
help_info = "'zip_submit AssignmentN_Name directory' submits AssignmentN_Name.zip on ada.evergreen.edu."
case_sensitive = True
command_name = 'zip_submit'

def csf_submit(self, args):
    print('csf_submit')
    folder = args[1]
    # for windows computers, the path separator is '\'. This section of code replaces all '\'s in the path name with '\\', so that it can actually be used
    if os.name is 'nt':
        folder = folder.split('\\')
        while len(folder) > 1:
            folder[0]=folder[0]+'\\'+folder[1]
            folder.pop(1)
        print(folder)
    # zip the files in the directory at the supplied path into a folder named args[0]
    zip_name = args[0] + '.zip'
    assignment = zipfile.ZipFile(zip_name, 'a')
    for root, directories, files in os.walk(folder[0]):
        for file in files:
            a = open(root + '\\' + file)
            assignment.write(a.name)
            a.close()
    assignment.close()
    

