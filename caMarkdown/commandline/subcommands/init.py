from ...dirHanders import makeProjectDir
import argparse
import sys

def initArgParse():
    parser = argparse.ArgumentParser(prog = ' '.join(sys.argv[:2]), description="caMarkdown's directory intilizer")
    parser.add_argument("dir", type = str, help = "The directory for caMarkdown to inilize in")
    return parser.parse_args(sys.argv[2:])

def startInit():
    args = initArgParse()
    makeProjectDir(args.dir)
