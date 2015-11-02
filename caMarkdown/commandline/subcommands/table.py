from .status import proccessFiles
from ...dirHanders import isCaDir, getIndexedFiles

import argparse
import sys
import collections

def tableArgParse():
    parser = argparse.ArgumentParser(prog = ' '.join(sys.argv[:2]), description="caMarkdown's table displayer")
    parser.add_argument("tags", nargs = '+', type = str, help = "The tags to be tablulated")
    return parser.parse_args(sys.argv[2:])

def startTable():
    args = tableArgParse()
    if not isCaDir():
        print("This is not caMarkdown directory, run `camd init` to make it one")
    else:
        codes = proccessFiles(getIndexedFiles(), verbose = False)
        tagsDict = collections.OrderedDict()
        for tag in args.tags:
            tagsDict[tag] = []
        for code in codes:
            if code.tag in args.tags:
                tagsDict[code.tag].append(code)
        titles = []
        lengths = []
        overlaps = []
        for tag, values in tagsDict.items():
            titles.append(tag)
            l = 0
            for v in values:
                l += len(v)
            lengths.append(str(l))
            overlp = ["{} overlap".format(tag)]
            for tag2 in tagsDict.keys():
                overlapSum = 0
                for v in values:
                    overlapSum += sum([len(v2) for v2 in v[tag2]])
                overlp.append(str(overlapSum))
            overlp = '\t'.join(overlp)
            overlaps.append(overlp)



        print("Tags    \t{}".format('\t'.join(titles)))
        print("Lengths \t{}".format('\t'.join(lengths)))
        for oString in overlaps:
            print(oString)
