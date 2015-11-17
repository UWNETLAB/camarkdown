import argparse
import sys
import os
import pathlib
from ...project import Project
from ...dirHanders import findTopDir
from ...caExceptions import UninitializedDirectory, ProjectFileError


def startArgParse():
    parser = argparse.ArgumentParser(prog = ' '.join(sys.argv[:2]), description="Add files to caMarkdown's index")
    parser.add_argument("paths", nargs = "+",type = str, help = "The paths of files or directories to be added")
    return parser.parse_args(sys.argv[2:])

def startAdd():
    args = startArgParse()
    try:
        caDir = findTopDir('.')
    except UninitializedDirectory:
        print("This is not caMarkdown repository or inside one.\nRun `camd init` to make it one")
    else:
        Proj = Project(caDir)
        for pStr in args.paths:
            try:
                path = pathlib.Path(pStr).resolve()
            except FileNotFoundError:
                print("{} doe not exist, skipping".format(pStr))
            else:
                if path not in Proj.getFiles():
                    print("Adding {}".format(path))
                    try:
                        Proj.addFile(path)
                    except ProjectFileError as e:
                        print("An error occured:", end = ' ')
                        print(e)
                else:
                    print("{} already in the code book skipping".format(path))
