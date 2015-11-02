from .codes import Code, makeCode, Node

def tokenizer2(s):
    tokens = []
    currentString = ''
    sIter = enumerate(s.__iter__())
    inBraces = False
    stopIter = False
    while not stopIter:
        try:
            i, char = next(sIter)
        except StopIteration:
            stopIter = True
            if len(currentString) > 0:
                tokens.append((currentString, i))
        else:
            if inBraces:
                if char == ')':
                    currentString += char
                    inBraces = False
                    tokens.append((currentString, i))
                    currentString = ''
                else:
                    currentString += char
            elif char == '[':
                if len(currentString) > 0:
                    tokens.append((currentString, i))
                    currentString = ''
                tokens.append((char , i))
            elif char == ']':
                if len(currentString) > 0:
                    tokens.append((currentString, i))
                    currentString = ''
                tokens.append((char, i))
                try:
                    i, char = next(sIter)
                except StopIteration:
                    stopIter = True
                else:
                    currentString += char
                    if char == '(':
                        inBraces = True
            else:
                currentString += char
    print("DSDSFDFSGFD")
    return tokens


def tokenizer(s):
    """Takes in a string and for every []() creates a Code object that knows the index of its braces.
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

def lineAndIndexCounter(targtString):
    sIter = enumerate(targtString.__iter__())
    lineCount = 1
    while True:
        i, char = next(sIter)
        if char == '\n':
            lineCount += 1
        yield lineCount, i, char

def getParseTree(targetString):
    codes = []
    sIter = lineAndIndexCounter(targetString)
    return Node(sIter, 0, -1, '')

def getTags(targetString):
    tree = getParseTree(targetString)
    return tree.tags
