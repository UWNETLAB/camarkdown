import argparse
import sys
import os
from ...dirHanders import isCaDir
from ...parser import getCodes
from ...codes import metaCode, contentCode, contextCode, metaChar, contentChar, contextChar

def statusArgParse():
    parser = argparse.ArgumentParser(prog = ' '.join(sys.argv[:2]), description="caMarkdown's status display")
    parser.add_argument("files", nargs = '*', type = str, help = "The The files for the stats to be run on.", default = [])
    return parser.parse_args(sys.argv[2:])

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


def startStatus():
    args = statusArgParse()
    codes = []
    if len(args.files) < 1:
        codes = proccessFiles([f for f in os.listdir('.') if os.path.isfile(f)])
    else:
        codes = proccessFiles(args.files)
