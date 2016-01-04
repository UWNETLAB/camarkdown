import sys

from .subCommandBase import baseArgparse, CommandOutputHandler, generalExceptionHandler

from ...project import Project
from ...caExceptions import UninitializedDirectory
from ...dirHanders import findTopDir

def organizeArgParse():
    parser = baseArgparse("caMarkdown's automated codebook organizer ")
    return parser.parse_args(sys.argv[2:])

def startOrganize():
    args = organizeArgParse()
    try:
        with CommandOutputHandler(args.output) as writer:
            try:
                caDir = findTopDir('.')
            except UninitializedDirectory:
                print("This is not caMarkdown repository or inside one.\nRun `camd init` to make it one")
            else:
                Proj = Project(caDir)
                writer("organizing codebook\n")
                Proj.organizeCodebook()
    except Exception as e:
        #Prettify things if they go bad
        generalExceptionHandler(e, args.debug)
