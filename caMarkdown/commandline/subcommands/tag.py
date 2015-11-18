import argparse
import sys
import os

from ...project import Project
from ...caExceptions import UninitializedDirectory
from ...dirHanders import findTopDir

def tagArgParse():
    parser = argparse.ArgumentParser(prog = ' '.join(sys.argv[:2]), description="caMarkdown's sync client")
    parser.add_argument("tag", nargs = '?', type = str, help = "The tag being queried.", default = None)
    return parser.parse_args(sys.argv[2:])

def startTag():
    args = tagArgParse()
    try:
        caDir = findTopDir('.')
    except UninitializedDirectory:
        print("This is not caMarkdown repository or inside one.\nRun `camd init` to make it one")
    else:
        Proj = Project(caDir)
        if args.tag is None:
            print("No tag specified, listing all tags:")
            for tag in Proj.codes.values():
                print(str(tag))
        elif args.tag in Proj.codes:
            targetCode = Proj.codes[args.tag]
            print("Getting the information on {}".format(args.tag))
            print(str(targetCode))
            print("The tag is used for the following pieces of text:")
            for sec in targetCode.sections:
                print(str(sec))
        else:
            print("{} is not in any of the documents or in the codebook.\nRun `camd tag` to get a list of all the tags.".format(args.tag))
