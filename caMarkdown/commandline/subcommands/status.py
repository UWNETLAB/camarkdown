import argparse
import sys
import os
from ...dirHanders import isCaDir, getIndexedFiles
from ...parser import getTags
from ...codes import metaCode, contentCode, contextCode, metaChar, contentChar, contextChar

def statusArgParse():
    parser = argparse.ArgumentParser(prog = ' '.join(sys.argv[:2]), description="caMarkdown's status display")
    return parser.parse_args(sys.argv[2:])

def proccessFiles(targetFilePaths):
    codes = []
    print("{} files given, parsing".format(len(targetFilePaths)))
    openFiles = []
    #Not using a closure so that all the files can be opened before parsing
    #If an error occurs it is likely to happen at open
    #Not reading after open as that uses more memory then this way
    goodFiles = 0
    badFiles = 0
    for fpath in targetFilePaths:
        try:
            openFiles.append(fpath.open('r'))
        except OSError:
            print("{} is not a valid file".format(str(fpath)))
            sys.exit()
    while len(openFiles) > 0:
        f = openFiles.pop()
        try:
            codes += getTags(f.read())
        except UnicodeDecodeError:
            badFiles += 1
        else:
            goodFiles += 1
        f.close()
    print("{} files parsed out of {} parsed".format(goodFiles, len(targetFilePaths)))
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


def startStatus():
    args = statusArgParse()
    if not isCaDir():
        print("This is not caMarkdown directory, run `camd init` to make it one")
    else:
        codes = proccessFiles(getIndexedFiles())
        print(codeStats(codes))
