import sys
import collections

from .subCommandBase import baseArgparse, CommandOutputHandler, generalExceptionHandler

from ...dirHanders import findTopDir
from ...caExceptions import UninitializedDirectory
from ...project import Project

def tableArgParse():
    parser = baseArgparse("caMarkdown's table displayer")
    parser.add_argument("tags", nargs = '+', type = str, help = "The tags to be tablulated")
    return parser.parse_args(sys.argv[2:])

def startTable():
    args = tableArgParse()
    try:
        with CommandOutputHandler(args.output) as writer:
            try:
                caDir = findTopDir('.')
            except UninitializedDirectory:
                print("This is not caMarkdown repository or inside one.\nRun `camd init` to make it one")
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
                        overlaps.append('\t'.join(overlp))
                    writer("Tags    \t{}\n".format('\t'.join(titles)))
                    writer("Lengths \t{}\n".format('\t'.join(lengths)))
                    for oString in overlaps:
                        writer(oString + '\n')
                else:
                    writer("No usable tags provided, please provide at least one to get a table.")
    except Exception as e:
        #Prettify things if they go bad
        generalExceptionHandler(e, args.debug)
