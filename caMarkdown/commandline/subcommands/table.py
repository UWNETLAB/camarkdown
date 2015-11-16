from ...dirHanders import isCaDir, getIndexedFiles, findTopDir
from ...caExceptions import UninitializedDirectory
from ...project import Project


import argparse
import sys
import collections

def tableArgParse():
    parser = argparse.ArgumentParser(prog = ' '.join(sys.argv[:2]), description = "caMarkdown's table displayer")
    parser.add_argument("tags", nargs = '+', type = str, help = "The tags to be tablulated")
    return parser.parse_args(sys.argv[2:])

def startTable():
    args = tableArgParse()
    try:
        caDir = findTopDir('.')
    except UninitializedDirectory:
        print("This is not caMarkdown repository or inside one, run `camd init` to make it one")
    else:
        Proj = Project(caDir)
        codes = Proj.getCodes()
        tagsDict = collections.OrderedDict()
        for tag in args.tags:
            try:
                tagsDict[tag] = codes[tag]
            except KeyError:
                print("'{}' is not a tag in the codebook or the text, it cannot be used in a table, it will be skipped.".format(tag))
        if len(tagsDict) > 0:
            titles = []
            lengths = []
            overlaps = []
            for tagString, tag in tagsDict.items():
                titles.append(tagString)
                lengths.append(str(len(tag)))
                overlp = ["{} overlap".format(tagString)]
                for tag2String in tagsDict.keys():
                    overlp.append(str(sum((len(v2) for v2 in tag[tag2String]))))
                overlp = '\t'.join(overlp)
                overlaps.append(overlp)
            print("Tags    \t{}".format('\t'.join(titles)))
            print("Lengths \t{}".format('\t'.join(lengths)))
            for oString in overlaps:
                print(oString)
        else:
            print("No usable tags provided, please provide at least one to get a table.")
