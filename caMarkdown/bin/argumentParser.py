import argparse

def argumentParser():
    parser = argparse.ArgumentParser(description="caMarkdown's command line interface")
    parser.add_argument("files", nargs = '+', type = argparse.FileType('r'), help = "The files for caMarkdown to run on.")
    return parser.parse_args()
