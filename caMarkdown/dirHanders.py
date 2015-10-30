from .defaultFiles import defaultCookbook, codeBookFileName, defaultConf, confFileName
from .caExceptions import AddingException
import os
import shutil
import pathlib

hiddenDirName = '.camd'
filesListName = 'caFiles'

def isCaDir():
    return os.path.isdir(hiddenDirName)

def makeCodeBookFile(targetFilePath):
    with open(targetFilePath, 'w') as target:
        target.write(defaultCookbook)

def makeConfFile(targetFilePath):
    with open(targetFilePath, 'w') as target:
        target.write(defaultConf)

def makeHiddenDir():
    os.mkdir(hiddenDirName)
    with open(os.path.join(hiddenDirName, filesListName), 'w') as f:
        f.write("")

def addFile(Path):
    for parent in Path.parents:
        if parent.name == hiddenDirName:
            raise AddingException("Adding a file from {}".format(hiddenDirName))
    with open(os.path.join(hiddenDirName, filesListName), 'a') as f:
        f.write(str(Path) + '\n')

def addPath(Path):
    if Path.exists():
        if Path.is_file():
            try:
                addFile(Path)
            except AddingException:
                pass
        elif Path.is_dir():
            for P in Path.iterdir():
                addPath(P)
        else:
            pass

def getIndexedFiles():
    paths = []
    with open(os.path.join(hiddenDirName, filesListName), 'r') as f:
        for line in f:
            paths.append(pathlib.Path(line.rstrip()))
    return paths

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
    if freshDir or not os.path.isdir(hiddenDirName):
        makeHiddenDir()
    #git init
