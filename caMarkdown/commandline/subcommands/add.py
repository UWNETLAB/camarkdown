import argparse
import sys
import os
import pathlib

from .subCommandBase import baseArgparse, CommandOutputHandler, generalExceptionHandler

from ...project import Project
from ...dirHanders import findTopDir
from ...caExceptions import UninitializedDirectory, ProjectFileError


def startArgParse():
    parser = baseArgparse("caMarkdown's codebook adding client")
    parser.add_argument("paths", nargs = "+",type = str, help = "The paths of files or directories to be added")
    return parser.parse_args(sys.argv[2:])

def startAdd():
    args = startArgParse()
    try:
        with CommandOutputHandler(args.output) as writer:
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
                        writer("{} doe not exist, skipping\n".format(pStr))
                    else:
                        if path not in Proj.getFiles():
                            writer("Adding {}\n".format(path))
                            try:
                                Proj.addFile(path)
                            except ProjectFileError as e:
                                print("An error occured:", end = ' ')
                                print(e)
                        else:
                            writer("{} already in the code book skipping\n".format(path))
    except Exception as e:
        #Prettify things if they go bad
        generalExceptionHandler(e, args.debug)
