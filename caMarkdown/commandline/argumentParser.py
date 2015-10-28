import argparse
import sys
from .subcommands import subCommands

def argumentParser():
    helpParser = argparse.ArgumentParser(description="caMarkdown's command line interface")
    return helpParser.parse_args()

def cli():
    if len(sys.argv) > 1 and sys.argv[1] in subCommands:
        subCommands[sys.argv[1]]()
    else:
        args = argumentParser()
        s = "The available commands are:\n\t{}\n".format('\n\t'.join(subCommands.keys()))
        s += "Run any of those with -h for help on it"
        print(s)
    #codes = proccessFiles(args.files)
    #while True:
    #    getAction(codes)
