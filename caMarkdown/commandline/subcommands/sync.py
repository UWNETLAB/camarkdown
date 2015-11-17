import argparse
import sys
import os

from ...project import Project
from ...caExceptions import UninitializedDirectory
from ...dirHanders import findTopDir

def syncArgParse():
    parser = argparse.ArgumentParser(prog = ' '.join(sys.argv[:2]), description="caMarkdown's sync client")
    parser.add_argument("tags", nargs = '*', type = str, help = "The tags to be synced")
    #parser.add_argument("--description", '-d', nargs = '+', type = str, help = "The descriptions of the tags to be synced")
    #Needs to be rethought as interface currently does not work
    return parser.parse_args(sys.argv[2:])

def startSync():
    args = syncArgParse()
    try:
        caDir = findTopDir('.')
    except UninitializedDirectory:
        print("This is not caMarkdown repository or inside one.\nRun `camd init` to make it one")
    else:
        Proj = Project(caDir)
        codes = Proj.getCodes()
        if len(args.tags) < 1:
            unDocumented = []
            for tag, code in codes.items():
                if code.unDocumented:
                    unDocumented.append(tag)
            if len(unDocumented) > 0:
                for tag in unDocumented:
                    Proj.addCode(tag)
                print("There are {} codes in the documents not in the codebook.  They are:\n\t{}\nThey have been added to the codebook.".format(len(unDocumented), '\n\t'.join(unDocumented)))
            else:
                print("All codes in the documents are in the codebook.")
        else:
            for tag in args.tags:
                Proj.addCode(tag)
                print("{} added to the codebook.".format(tag))
