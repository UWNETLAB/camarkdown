import argparse
import sys
import os

from ...project import Project
from ...dirHanders import isCaDir, getIndexedFiles, findTopDir
from ...parser import getTags
from ...codes import MetaCodeSection, ContentCodeSection, ContextCodeSection, metaChar, contentChar, contextChar
from ...caExceptions import UninitializedDirectory

def statusArgParse():
    parser = argparse.ArgumentParser(prog = ' '.join(sys.argv[:2]), description="caMarkdown's status display")
    return parser.parse_args(sys.argv[2:])

def startStatus():
    args = statusArgParse()
    try:
        caDir = findTopDir('.')
    except UninitializedDirectory:
        print("This is not caMarkdown repository or inside one, run `camd init` to make it one")
    else:
        Proj = Project(caDir)
        codes = Proj.getCodes()
        print("This project has {} codes.".format(len(codes)))
        unCommented = {}
        commented = {}
        unDocumented = {}
        unUsed = {}
        for tag, code in codes.items():
            if len(code.sections) < 1:
                unUsed[tag] = code
            if code.unDocumented:
                unDocumented[tag] = code
            elif code.comment:
                commented[tag] = code
            else:
                unCommented[tag] = code
        if len(unDocumented) > 0:
            print("There are {} codes not in the codebook used in the texts. They are:\n\t{}".format(len(unDocumented), '\n\t'.join(unDocumented.keys())))
        if len(unCommented) > 0:
            print("There are {} codes in the codebook without any description. They are:\n\t{}".format(len(unCommented), '\n\t'.join(unCommented.keys())))
        if len(unUsed) > 0:
            print("There are {} codes in the codebook not used in the text. They are:\n\t{}".format(len(unUsed), '\n\t'.join(unUsed.keys())))
        if len(commented) > 0:
                print("There are {} codes in the codebook with a description.".format(len(commented)))
