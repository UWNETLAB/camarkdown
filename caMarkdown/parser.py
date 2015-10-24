from .codes import Code, makeCode



def tokenizer(s):
    """Takes in a string and for every []() creates a Code object that know the index of its braces.
    """
    openIndices = []
    closedTags = []
    sIter = enumerate(s.__iter__())
    stopIter = False
    while not stopIter:
        #Need to use the variable stopIter as different things can stop the loop
        try:
            i, char = next(sIter)
        except StopIteration:
            stopIter = True
        else:
            if char == '[':
                openIndices.append(i)
            if char == ']' and len(openIndices) > 0:
                try:
                    i, char = next(sIter)
                except StopIteration:
                    stopIter = True
                    char = ''
                openBraceIndex = openIndices.pop()
                closeBraceIndex = i - 1
                codeStr = ''
                if char == '(':
                    try:
                        while True:
                            i, char = next(sIter)
                            if char == ')':
                                currentTag = makeCode(openBraceIndex, closeBraceIndex, i, codeStr, s)
                                break
                            else:
                                codeStr += char
                    except StopIteration:
                        stopIter = True
                    else:
                        closedTags += currentTag
                else:
                    pass
    return closedTags

def cutString(s, cutLst):
    """Takes a string an a series of indices to cut on and returns a list of tuples with the first element being the start of the cut and the second the string
    """

    retStrings = []
    cutLst = sorted(cutLst, key = lambda x: x[0], reverse = True)
    lastStart = len(s)
    for start, stop in cutLst:
        retStrings.append((stop,s[stop:lastStart]))
        lastStart = start
    retStrings.append((0, s[0:lastStart]))
    retStrings.reverse()
    return retStrings

def getCodes(string):
    baseCodes = tokenizer(string)
    cuts = []
    for code in baseCodes:
        if code.isCode:
            cuts += code.getCutIndices()
    choppedString = cutString(string, cuts)
    for code in baseCodes:
        s = ''
        for startString, stringVal in choppedString:
            if startString < code.startIndex:
                pass
            elif startString < code.closeIndex:
                s += stringVal
            else:
                break
            code.contents = s
    return baseCodes
