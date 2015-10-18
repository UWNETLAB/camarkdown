from codes import Code
blockChar = '^'
bracketChars = set(['(', ')', '[', ']'])

def tokenizer(s):
    openTags = []
    closedTags = []
    sIter = enumerate(s.__iter__())
    stopIter = False
    while not stopIter:
        try:
            i, char = next(sIter)
        except StopIteration:
            stopIter = True
        else:
            print(char, end = '')
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

print(tokenizer(open("tests/RecordTarget.md").read()))


"""
def tokenizer(s):
    tokens = []
    openBraces = 0
    offset = 0
    mostRecentOpenBrace = None
    reducedString = ''
    sIter = enumerate(s.__iter__())
    while True:
        try:
            i, char = next(sIter)
        except StopIteration:
            break
        if char == '[':
            openBraces += 1
            mostRecentOpenBrace = len(tokens)
            tokens.append((i + offset, char))
        elif char == ']' and openBraces > 0:
            try:
                i, nxtChar = next(sIter)
            except StopIteration:
                pass#TODO FIX <------------------
            if nxtChar == '(':
                tokens.append((i - 1 + offset, "](" + getContents(sIter)))
                openBraces -= 1
            else:
                openIndex, openString = tokens.pop(mostRecentOpenBrace)[0]
                reducedString = reducedString[:openIndex] + openString + reducedString[openIndex:] + char
                offset += len(openString)
                for i in range(len(tokens) - mostRecentOpenBrace):
                    index, brace = tokens[mostRecentOpenBrace + i]
                    tokens[mostRecentOpenBrace + i] = (index + len(openString), brace)
        else:
            reducedString += char
    return tokens, reducedString

def getContents(contIter):
    i, currentChar = next(contIter)
    retConts = currentChar
    while currentChar != ')':
        #TODO Solve case of this not closing
        i, currentChar = next(contIter)
        retConts += currentChar
    return retConts



def caParser(target):
    print(type(target))
    targetIter = enumerate(target.__iter__())
    while True:
        try:
            print(jumpToBrackets(targetIter))
        except StopIteration:
            break

def fileParse(target, master):
    with open(target) as fTarget:
        print(fTarget.read())
        caParser(fTarget.read())

def jumpToBrackets(targetIter):
    while True:
        charNum, char = next(targetIter)
        if char not in bracketChars:
            pass
        else:
            return charNum, char
"""
