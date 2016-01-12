import pathlib
import random
import shutil
import os.path

from ..caExceptions import TestError
from ..codes import codeSectionTypes

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

def copyToRandomDir(startingPath, target, writeCodes, sectionsCount):
    currentPath = startingPath
    done = False
    while not done:
        i = random.randint(0, 10)
        if i > 7:
            if writeCodes:
                with open(str(target)) as fTarget:
                    with open(str(pathlib.Path(currentPath, target.name)), 'x') as fResult:
                        s = addCodes(fTarget.read(), sectionsCount, 20)[2]
                        fResult.write(s)
            else:
                shutil.copy2(str(target), str(pathlib.Path(currentPath, target.name)))
            done = True
        else:
            try:
                currentPath = pathlib.Path(currentPath, random.choice([i for i in currentPath.iterdir() if i.is_dir()]))
            except IndexError:
                if writeCodes:
                    with open(str(target)) as fTarget:
                        with open(str(pathlib.Path(currentPath, target.name)), 'x') as fResult:
                            s = addCodes(fTarget.read(), sectionsCount, 20)[2]
                            fResult.write(s)
                else:
                    shutil.copy2(str(target), str(pathlib.Path(currentPath, target.name)))
                done = True

def makeTestDir(name, targetfileDir, dirCount = 10, maxDepth = 10, writeCodes = False, sectionsCount = 20, overwrite = False):
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
        if overwrite:
            shutil.rmtree(name)
            base.mkdir()
            base = pathlib.Path(name).resolve()
        else:
            raise TestError("Root directory creation failed, This function can only be run to create a new directory in an existing location. The directory {} is already exists.".format(targetfileDir))

    except FileNotFoundError:
        raise TestError("Root directory creation failed, This function can only be run to create a new directory in an existing location. The some of the parents of {} is do not exist.".format(targetfileDir))
    for i in range(dirCount):
        makeRandomDir(base, maxDepth)
    for target in targets:
        copyToRandomDir(base, target, writeCodes, sectionsCount)

def _quickTestDirMake():
    makeTestDir('tempDir', os.path.join(os.path.dirname(__file__), 'womenInComp'))

def inRange(num, rang):
    return num <= rang[0] or num >= rang[1]

def getStartStop(AllowedRanges, maxIndex):
        start = random.randint(0, maxIndex)
        end = random.randint(0, maxIndex)
        if start == end:
            return getStartStop(AllowedRanges, maxIndex)
        elif start > end:
            start, end = end, start
        for r in AllowedRanges:
            if inRange(start, r) and not inRange(end, r):
                return getStartStop(AllowedRanges, maxIndex)
        return start, end

def generateCodes(codeCount):
    retCodes = []
    codesCharLst = list(codeSectionTypes.keys())
    for i in range(codeCount):
        codeType = random.choice(codesCharLst)
        codeString = randomString().lower()
        retCodes.append(codeType + codeString)
    return retCodes

def generateBraces(codes):
    retLst = []
    length = 0
    retLst.append('](')
    retLst.append('{}'.format(random.choice(codes)))
    while random.randint(0, 1) == 1:
        retLst[1]+= ' {}'.format(random.choice(codes))
    retLst.append(')')
    return retLst, len(retLst[1]) + 3

def addCodes(targetString, sectionsCount, codeCount):
    maxIndex = len(targetString) - 1
    starts = []
    ends = []
    ranges = []
    codes = generateCodes(codeCount)
    for i in range(sectionsCount):
        s, e = getStartStop(ranges, maxIndex)
        ranges.append((s, e))
        starts.append(s)
        ends.append(e)
    inserts = {}
    currentPos = 0
    splitString = []
    previousSplit = 0
    for i in sorted(starts + ends):
        splitString.append(targetString[previousSplit : i])
        currentPos += i - previousSplit
        previousSplit = i
        if i in ends:
            bStrings, lengMod = generateBraces(codes)
            inserts[currentPos] = bStrings[1]
            currentPos += lengMod
            splitString += bStrings
        else:
            splitString.append('[')
            inserts[currentPos] = ''
            currentPos += 1
    splitString.append(targetString[previousSplit : maxIndex])
    return starts, inserts, ''.join(splitString)
