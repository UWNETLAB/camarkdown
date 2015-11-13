from .defaultFiles import defaultCookbook, codeBookFileName, defaultConf, confFileName
from .caExceptions import AddingException, UninitializedDirectory
import os
import shutil
import pathlib
import dulwich.repo
import dulwich.errors

hiddenDirName = '.camd'
filesListName = 'caFiles'

def findTopDir(startPath):
    workingpath = startPath.resolve()
    if not workingpath.is_dir():
        workingpath = workingpath.parent()
    while workingpath.parent != workingpath:
        if len(workingpath.glob('.git')) > 0:
            return workingpath
        else:
            workingpath = workingpath.parent
    raise UninitializedDirectory("{} is not a caMarkdown directory and none of its parents are either.".format(startPath))



def makeGitignore():
    with open('.gitignore', 'w') as target:
        target.write("#Put the files you want nothing to track here:\n")

def makeCAignore():
    with open('.camdignore', 'w') as target:
        target.write("#Put the files you do not want caMarkdown to track here:\n")
        target.write("#By default only those ending in .md or .markdown are tracked\n\n")
        target.write("*\n\n")
        target.write("!*.md\n")
        target.write("!*.markdown\n")

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
    dirPath = pathlib.Path(dirName)
    freshDir = True
    try:
        dirPath.mkdir(parents = True)
        #Not using exist_ok as that can still raise exceptions
        #https://bugs.python.org/issue21082
    except OSError:
        freshDir = False
    try:
        os.chdir(str(dirPath))
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
    try:
        Repo = dulwich.repo.Repo('.')
    except dulwich.errors.NotGitRepository:
        Repo = dulwich.repo.Repo.init('.')
    makeGitignore()
    makeCAignore()
