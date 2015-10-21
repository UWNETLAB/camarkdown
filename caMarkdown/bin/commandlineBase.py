import argparse
from .argumentParser import argumentParser
from ..parser import getCodes

def cli():
    args = argumentParser()
    for f in args.files:
        print(getCodes(f.read()))
