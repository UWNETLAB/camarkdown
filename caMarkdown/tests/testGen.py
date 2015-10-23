import random
from ..codes import Code, makeCode

def makeTestFile(inputString, numCuts, numTags, numBlocks, maxTagLen = 16, maxTagPerBlock = 5):
    tags = []
    cuts = []
    blocks = []
    for i in range(numTags):
        #Make numTags random strigns of numbers
        tmpTag = str(random.randrange(10 ** (maxTagLen + 1) - 1))
        while tmpTag in tags:
            tmpTag = str(random.randrange(10 ** (maxTagLen + 1) - 1))
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
    rawCodes = {}
    for i in range(numBlocks):
        #Make numBlocks groups of cuts to make the blocks around
        try:
            startBlock = cuts.pop()
        except IndexError:
            break
        try:
            stopblock = cuts.pop()
        except IndexError:
            cuts.append(startBlock)
            break
            #If not enough cuts stop
        codeTags = []
        for i in range(random.randrange(maxTagPerBlock)):
            #Give the block some tags
            codeTags.append(random.choice(tags))
        if len(codeTags) > 0:
            codeTags = "^{}".format(' ^'.join(codeTags))
            rawCodes[startBlock] = (stopblock, codeTags)
            rawCodes[stopblock] = (startBlock, codeTags)
        else:
            rawCodes[startBlock] = "["
            rawCodes[stopblock] = "]"
    for cut in cuts:
        rawCodes[cut] = None
    retString = ''
    codes = []
    for i, cut in enumerate(sorted(rawCodes.keys())):
        cutVal = rawCodes[cut]
        if cutVal is None:
            retString += splitString[i]
        elif isinstance(cutVal, str):
            retString += splitString[i] + cutVal
        else:
            if cutVal[0] > cut:
                retString +=  splitString[i] + "["
                rawCodes[cut] = len(retString)
            else:
                retString +=  splitString[i] + "]"
                blockIndex = len(retString)
                retString += "({})".format(cutVal[1])
                codes += makeCode(rawCodes[cutVal[0]], blockIndex, len(retString), cutVal[1])
    return retString
