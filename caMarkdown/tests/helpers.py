import pathlib
import random
import shutil
import os.path

from ..caExceptions import TestError

def randomString():
    remainingChars = 20
    retString = ''
    while remainingChars > 0:
        retString += chr(random.randint(65,90))
        remainingChars -= random.randint(1,3)
    return retString

def makeRandomDir(startingPath, maxDepth):
    depth = 0
    retPath = startingPath
    while depth < maxDepth:
        try:
            if random.randint(0, 10) > 7:
                #less code than branching
                raise TestError("This should always be caught, tell whomever is manging this if it is not.")
            retPath = pathlib.Path(retPath, random.choice([i for i in retPath.iterdir()]))
            depth += 1
        except (IndexError, TestError, FileNotFoundError):
            retPath = pathlib.Path(retPath, randomString())
            depth += random.randint(1, maxDepth)
    retPath.mkdir(parents = True)

def copyToRandomDir(startingPath, target):
    currentPath = startingPath
    done = False
    while not done:
        i = random.randint(0, 10)
        if i > 7:
            shutil.copy2(str(target), str(pathlib.Path(currentPath, target.name)))
            done = True
        else:
            try:
                currentPath = pathlib.Path(currentPath, random.choice([i for i in currentPath.iterdir() if i.is_dir()]))
            except IndexError:
                shutil.copy2(str(target), str(pathlib.Path(currentPath, target.name)))
                done = True

def makeTestDir(name, targetfileDir, dirCount = 10, maxDepth = 10):
    base = pathlib.Path(name)
    try:
        #Testing before files and dirs are created as speed is not a concern
        targets = (f for f in pathlib.Path(targetfileDir).iterdir())
    except (IndexError, FileNotFoundError):
        raise TestError("The target files directory is empty or does not exist. files are required for this function.")
    try:
        base.mkdir()
        base = pathlib.Path(name).resolve()
    except FileExistsError:
        raise TestError("Root directory creation failed, This function can only be run to create a new directory in an existing location. The directory {} is already exists.".format(targetfileDir))
    except FileNotFoundError:
        raise TestError("Root directory creation failed, This function can only be run to create a new directory in an existing location. The some of the parents of {} is do not exist.".format(targetfileDir))
    for i in range(dirCount):
        makeRandomDir(base, maxDepth)
    for target in targets:
        copyToRandomDir(base, target)

def _quickTestDirMake():
    makeTestDir('tempDir', os.path.join(os.path.dirname(__file__), 'womenInComp'))
