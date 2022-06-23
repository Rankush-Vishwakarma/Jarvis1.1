# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 20:56:04 2022

@author: rvishwakar23
"""

import os
import shutil

def fileCopier(filetype):
    print(f"Please wait i'm loading the {filetype} files")
    fileList = []
    mainFolders = []
    # getting the default base directory path
    dir_path = os.path.expanduser('~')
    #list all the directories 
    directories =  os.listdir(dir_path)
    # checking is the direcotory is not denied with permission.
    
    for i in directories:
        if '.' not in i and not i.startswith('__') and not i.endswith('__'):
            try:
                os.listdir(dir_path+'\\'+i)
                mainFolders.append(i)
            except PermissionError:
                pass
    # check for the files in all the folders.
    for root, _, files in os.walk(dir_path):
        if len( root.split('\\'))>3 and root.split('\\')[3] in mainFolders:
            for file in files:
                if file.endswith(f'.{filetype}'):
                    #print(file)
                    filePath = root+'\\'+str(file)
                    fileList.append(filePath)
                else:
                    pass
    return fileList

