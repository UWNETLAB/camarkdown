import argparse
import sys
import os

from .subCommandBase import baseArgparse, CommandOutputHandler, generalExceptionHandler

from ...project import Project
from ...caExceptions import UninitializedDirectory
from ...dirHanders import findTopDir

def tagArgParse():
    parser = baseArgparse("caMarkdown's tag manipulation client")
    parser.add_argument("tag", nargs = '?', type = str, help = "The tag being queried.", default = None)
    return parser.parse_args(sys.argv[2:])

def startTag():
    args = tagArgParse()
    try:
        with CommandOutputHandler(args.output) as writer:
            try:
                caDir = findTopDir('.')
            except UninitializedDirectory:
                print("This is not caMarkdown repository or inside one.\nRun `camd init` to make it one")
            else:
                Proj = Project(caDir)
                if args.tag is None:
                    writer("No tag specified, listing all tags:\n")
                    for tag in Proj.codes.values():
                        writer(str(tag) + "\n")
                elif args.tag in Proj.codes:
                    targetCode = Proj.codes[args.tag]
                    writer("Getting the information on {}\n".format(args.tag))
                    writer(str(targetCode) + '\n')
                    writer("The tag is used for the following pieces of text:\n")
                    for sec in targetCode.sections:
                        writer(str(sec) + '\n')
                else:
                    print("{} is not in any of the documents or in the codebook.\nRun `camd tag` to get a list of all the tags.".format(args.tag))
    except Exception as e:
        #Prettify things if they go bad
        generalExceptionHandler(e, args.debug)
