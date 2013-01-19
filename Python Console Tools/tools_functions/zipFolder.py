# zipFolder
# Plans:
# - prevent unnecessary subdirectories in the end .zip folder
#    currently the program will recreate the entire supplied path within the .zip, including directories who's only content is a single directory
#    this is unecessary and makes me feel bad about submitting the .zip on ada

import sys, os, zipfile
from os import path

def zipFolder(self, args):
    folder = args[1]
    # for windows computers, the path separator is '\'. This section of code replaces all '\'s in the path name with '\\', so that it can actually be used
    if os.name is 'nt':
        folder = folder.split('\\')
        while len(folder) > 1:
            folder[0]=folder[0]+'\\'+folder[1]
            folder.pop(1)
        folder = folder[0]
    folder = os.path.normpath(folder)
    # zip the files in the directory at the supplied path into a folder named args[0]
    zip_name = args[0] + '.zip'
    assignment = zipfile.ZipFile(zip_name, 'a')
    for root, directories, files in os.walk(folder):
        for file in files:
            a = open(root + '\\' + file)
            assignment.write(a.name)
            a.close()
    assignment.close()

func_alias = 'zip'
func_info = (zipFolder,
             2,
             2,
             "zip_submit: <Assignment_Name> <directory> creates a zip folder 'AssignmentN_Name.zip' in the directory you run it from",
             True,
             )
