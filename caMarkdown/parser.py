from .codes import Code

def tokenizer(s):
    """Takes in a string and for every []() creates a Code object that know the index of its braces.
    """
    openTags = []
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
                openTags.append(Code(s, i))
            if char == ']' and len(openTags) > 0:
                try:
                    i, char = next(sIter)
                except StopIteration:
                    stopIter = True
                    char = ''
                if char == '(':
                    currentTag = openTags.pop()
                    currentTag.closeText(i - 1)
                    currentTag.startBrace(i)
                    code = ''
                    try:
                        while True:
                            i, char = next(sIter)
                            if char == ')':
                                currentTag.closeBrace(i, code)
                                break
                            else:
                                code += char
                    except StopIteration:
                        stopIter = True
                    else:
                        closedTags.append(currentTag)
                else:
                    currentTag = openTags.pop()
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
            elif startString <= code.closeIndex:
                s += stringVal
            else:
                break
            code.contents = s
    return baseCodes
