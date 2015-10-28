from .defaultFiles import defaultCookbook, codeBookFileName, defaultConf, confFileName
import os
import shutil

def makeCodeBookFile(targetFilePath):
    with open(targetFilePath, 'w') as target:
        target.write(defaultCookbook)

def makeConfFile(targetFilePath):
    with open(targetFilePath, 'w') as target:
        target.write(defaultConf)

def makeProjectDir(dirName):
    freshDir = True
    try:
        os.makedirs(dirName)
        #Not using exist_ok as that can still raise exceptions
        #https://bugs.python.org/issue21082
    except OSError:
        freshDir = False
    try:
        os.chdir(dirName)
    except OSError:
        #TODO Consider how to handle this issue:
        #print()
        #custom except
        raise
    if freshDir or not os.path.isfile(codeBookFileName):
        makeCodeBookFile(codeBookFileName)
    if freshDir or not os.path.isfile(confFileName):
        makeConfFile(confFileName)
    #git init
