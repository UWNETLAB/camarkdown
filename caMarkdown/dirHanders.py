import os
import shutil

import dulwich.repo
import dulwich.errors


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

def isCaDir():
    return os.path.isdir(hiddenDirName)

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
