from ...project import Project
import argparse
import sys

def initArgParse():
    parser = argparse.ArgumentParser(prog = ' '.join(sys.argv[:2]), description="caMarkdown's directory intilizer")
    parser.add_argument("dir", nargs = "?", type = str, help = "The directory for caMarkdown to inilize in", default = '.')
    return parser.parse_args(sys.argv[2:])

def startInit():
    args = initArgParse()
    P = Project(args.dir)
    if P.bad:
        P.initializeDir()
        print("Initialized empty caMarkdown repository in {}".format(P.path))
    else:
        P.initializeDir()
        print("Reinitialized existing caMarkdown repository in {}".format(P.path))
