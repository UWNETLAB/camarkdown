"""import random
from ..codes import Code, makeCode

def makeTestFile(inputString, numCuts, numTags, numBlocks, maxTagLen = 16, maxTagPerBlock = 5):
    tags = []
    cuts = []
    blocks = []
    for i in range(numTags):
        #Make numTags random strigns of numbers
        tmpTag = str(random.randrange(10 ** (maxTagLen) - 1))
        while tmpTag in tags:
            tmpTag = str(random.randrange(10 ** (maxTagLen) - 1))
        tags.append(tmpTag)
    for i in range(numCuts):
        #Make numCuts random numbers to cut on
        cut = random.randrange(len(inputString))
        while cut in cuts:
            cut = random.randrange(len(inputString))
        cuts.append(cut)
    splitString = []
    recentCut = len(inputString)
    for cut in sorted(cuts, reverse = True):
        splitString.append(inputString[cut:recentCut])
        recentCut = cut
    splitString.append(inputString[0:recentCut])
    splitString.reverse()
    rawCodes = {cut : None for cut in cuts}
    for i in range(numBlocks):
        #Make numBlocks groups of cuts to make the blocks around
        try:
            block1 = cuts.pop()
        except IndexError:
            break
        try:
            block2 = cuts.pop()
        except IndexError:
            cuts.append(block1)
            break
            #If not enough cuts stop
        codeTags = []
        for i in range(random.randrange(maxTagPerBlock)):
            #Give the block some tags
            codeTags.append(random.choice(tags))
        if len(codeTags) > 0:
            codeTags = "^{}".format(' ^'.join(codeTags))
            rawCodes[block1] = (block2, codeTags)
            rawCodes[block2] = (block1, codeTags)
        else:
            if block1 < block2:
                rawCodes[block1] = "["
                rawCodes[block2] = "]"
            else:
                rawCodes[block1] = ")"
                rawCodes[block2] = "("
    retString = ''
    codes = []
    for cut in sorted(rawCodes.keys()):
        cutVal = rawCodes[cut]
        if cutVal is None:
            retString += splitString.pop(0)
        elif isinstance(cutVal, str):
            retString += splitString.pop(0) + cutVal
        else:
            if cutVal[0] > cut:
                retString +=  splitString.pop(0) + "["
                rawCodes[cut] = len(retString)
            else:
                retString +=  splitString.pop(0) + "]"
                blockIndex = len(retString)
                retString += "({})".format(cutVal[1])
                codes += makeCode(rawCodes[cutVal[0]] - 1, blockIndex - 1, len(retString), cutVal[1])
    while len(splitString) > 0:
        retString +=  splitString.pop(0)
    return (retString, codes)
"""
