import argparse
import sys

from .subCommandBase import baseArgparse, CommandOutputHandler, generalExceptionHandler

from ...project import Project

def initArgParse():
    parser = baseArgparse("caMarkdown's directory intilizer")
    parser.add_argument("dir", nargs = "?", type = str, help = "The directory for caMarkdown to intilize in", default = '.')
    return parser.parse_args(sys.argv[2:])

def startInit():
    args = initArgParse()
    try:
        with CommandOutputHandler(args.output) as writer:
            P = Project(args.dir)
            if P.bad:
                P.initializeDir()
                writer("Initialized empty caMarkdown repository in {}\n".format(P.path))
            else:
                P.initializeDir()
                writer("Reinitialized existing caMarkdown repository in {}\n".format(P.path))
    except Exception as e:
        #Prettify things if they go bad
        generalExceptionHandler(e, args.debug)
