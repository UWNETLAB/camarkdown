import argparse
import sys
import os

from .subCommandBase import baseArgparse, CommandOutputHandler, generalExceptionHandler

from ...project import Project
from ...dirHanders import isCaDir, getIndexedFiles, findTopDir
from ...parser import getTags
from ...codes import MetaCodeSection, ContentCodeSection, ContextCodeSection, metaChar, contentChar, contextChar
from ...caExceptions import UninitializedDirectory

def statusArgParse():
    parser = baseArgparse("caMarkdown's status display")
    return parser.parse_args(sys.argv[2:])

def makeStatusString(P):
    codes = P.getCodes()
    files = P.getFiles()
    allFiles = P.getAllTrackedFiles()
    s = "This project has {} codes and {} document(s).\n".format(len(codes), len(files))
    if len(files) < len(allFiles):
        untracked = []
        for fPath in allFiles:
            if fPath not in files:
                untracked.append(str(fPath.relative_to(P.path)))
        s += "There are {} untracked file(s). They are:\n\t{}\n".format(len(untracked), '\n\t'.join(untracked))
    unCommented = {}
    commented = {}
    unDocumented = {}
    unUsed = {}
    for tag, code in codes.items():
        if len(code.sections) < 1:
            unUsed[tag] = code
        if code.unDocumented:
            unDocumented[tag] = code
        elif code.description:
            commented[tag] = code
        else:
            unCommented[tag] = code
    if len(unDocumented) > 0:
        s += "There are {} code(s) not in the codebook used in the texts. They are:\n\t{}\n".format(len(unDocumented), '\n\t'.join(unDocumented.keys()))
    if len(unCommented) > 0:
        s += "There are {} code(s) in the codebook without any description. They are:\n\t{}\n".format(len(unCommented), '\n\t'.join(unCommented.keys()))
    if len(unUsed) > 0:
        s += "There are {} code(s) in the codebook not used in the text. They are:\n\t{}\n".format(len(unUsed), '\n\t'.join(unUsed.keys()))
    if len(commented) > 0:
            s += "There are {} code(s) in the codebook with a description.\n".format(len(commented))
    return s

def startStatus():
    args = statusArgParse()
    try:
        with CommandOutputHandler(args.output) as writer:
            try:
                caDir = findTopDir('.')
            except UninitializedDirectory:
                writer("This is not caMarkdown repository or inside one.\nRun `camd init` to make it one")
            else:
                Proj = Project(caDir)
                writer(makeStatusString(Proj))
    except Exception as e:
        #Prettify things if they go bad
        generalExceptionHandler(e, args.debug)
