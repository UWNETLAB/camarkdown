import argparse
import sys
import os
import pathlib
from ...dirHanders import addPath, isCaDir


def startArgParse():
    parser = argparse.ArgumentParser(prog = ' '.join(sys.argv[:2]), description="Add files to caMarkdown's index")
    parser.add_argument("paths", nargs = "+",type = str, help = "The paths of files or directories to be added")
    return parser.parse_args(sys.argv[2:])

def startAdd():
    args = startArgParse()
    if not isCaDir():
        print("Not caMarkdown directory\nExiting")
    else:
        for path in args.paths:
            print("Adding {}".format(path))
            addPath(pathlib.Path(path))
