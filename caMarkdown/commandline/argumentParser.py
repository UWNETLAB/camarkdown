import argparse
import sys

from .subcommands import subCommands

from .. import version

def argumentParser():
    helpParser = argparse.ArgumentParser(description="caMarkdown's command line interface", prog = sys.argv[0])
    helpParser.add_argument('--version', action = 'version', version = 'caMarkdown version {}'.format(version))
    return helpParser.parse_args()

def cli():
    if len(sys.argv) > 1 and sys.argv[1] in subCommands:
        subCommands[sys.argv[1]]()
    else:
        args = argumentParser()
        s = "The available commands are:\n\t{}\n".format('\n\t'.join(subCommands.keys()))
        s += "Run any of those with -h for help with it"
        print(s)
