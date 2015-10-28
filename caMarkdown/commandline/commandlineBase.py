import argparse
import readline
import collections
import sys
from .argumentParser import argumentParser
from ..parser import getCodes
from ..codes import metaCode, contentCode, contextCode, metaChar, contentChar, contextChar

def inputMenu(inputDict, header = None, footer = None, errorMsg = 'That is not an option please select a different value.', promptMsg = 'What is your selection: ', extraOptions = True):
    s = ''
    if header:
        s += '{}\n'.format(header)
    for k in inputDict.keys():
        s += '{0}) {1}\n'.format(k,inputDict[k])
    if extraOptions:
        s += 'q) quit\n'
    if footer:
        s += '{}\n'.format(footer)
    print(s, end = '')
    selection = input(promptMsg)
    if selection in inputDict:
        return selection
    elif extraOptions and selection == 'q':
        sys.exit()
    else:
        print(errorMsg)
        return inputMenu(inputDict, header = header, footer = footer, errorMsg = errorMsg, promptMsg = promptMsg)

def proccessFiles(targetFileNames):
    codes = []
    print("{} files given, parsing".format(len(targetFileNames)))
    openFiles = []
    #Not using a closure so that all the files can be opened before parsing
    #If an error occurs it is likely to happen at open
    #Not reading after open as that uses more memory then this way
    for fname in targetFileNames:
        try:
            openFiles.append(open(fname))
        except OSError:
            print("{} is not a valid file".format(fname))
            sys.exit()
    while len(openFiles) > 0:
        f = openFiles.pop()
        codes += getCodes(f.read())
        f.close()
    return codes

def codeStats(codes):
    metaCount, extCount, ontCount = 0, 0, 0
    for c in codes:
        if isinstance(c, metaCode):
            metaCount += 1
        elif isinstance(c, contentCode):
            ontCount += 1
        elif isinstance(c, contextCode):
            extCount += 1
        else:
            raise RunTimeError("{} is not a Code subclass".format(type(c)))
    s = "{} codes of divided into:\nmeta({}) {}\ncontent({}) {}\ncontext({}) {}".format(len(codes), metaChar, metaCount, contentChar, ontCount, contextChar, extCount)
    return s

def getAction(codes):
    actDict = collections.OrderedDict([
    ('1', "Display the stats of the codes"),
    ('2', "Go over the codes"),
    ])
    optionNum = int(inputMenu(actDict))
    if optionNum == 1:
        print(codeStats(codes))
