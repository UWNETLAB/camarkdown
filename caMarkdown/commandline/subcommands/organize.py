import argparse
import sys
import os

from ...project import Project
from ...caExceptions import UninitializedDirectory
from ...dirHanders import findTopDir

def organizeArgParse():
    parser = argparse.ArgumentParser(prog = ' '.join(sys.argv[:2]), description="orgaize the codebook")
    return parser.parse_args(sys.argv[2:])

def startOrganize():
    args = organizeArgParse()
    try:
        caDir = findTopDir('.')
    except UninitializedDirectory:
        print("This is not caMarkdown repository or inside one.\nRun `camd init` to make it one")
    else:
        Proj = Project(caDir)
        print("organizing codebook")
        Proj.organizeCodebook()
