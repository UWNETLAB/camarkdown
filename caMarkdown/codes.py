from .caExceptions import CodeParserException

contextChar = '@'
contentChar = '$'
metaChar = '^'

class Code2(object):
    def __init__(self, sIter):
        self.bad = False
        self.tokens = None
        self.contents = []

        stopIter = False
        inBraces = False
        currentString = ''

        while not stopIter:
            try:
                char = next(sIter)
                print(char, inBraces, sep = ' | ')
            except StopIteration:
                if inBraces:
                    currentString += '](' + self.tokens
                self.contents.append(currentString)
                self.bad = True
                stopIter = True
            else:
                if inBraces:
                    if char == ')':
                        stopIter = True
                    else:
                        self.tokens += char
                elif char == '[':
                    self.contents.append(currentString)
                    innerCode = Code2(sIter)
                    if innerCode.bad:
                        if len(innerCode.contents) < 1:
                            raise CodeParserException("Code has no contents")
                        else:
                            self.contents.append('[')
                            self.contents.append(innerCode.contents)
                            self.contents.append(']')
                    else:
                        self.contents.append(innerCode)
                elif char == ']':
                    try:
                        char = next(sIter)
                    except StopIteration:
                        stopIter = True
                    else:
                        if char == '(':
                            self.tokens = ''
                            inBraces = True
                            self.contents.append(currentString)
                        elif char == '[':
                            self.contents.append(Code2(sIter))
                            self.bad = True
                            stopIter = True
                        else:
                            currentString += ']' + char
                            self.contents.append(currentString)
                            stopIter = True
                            self.bad = True
                else:
                    currentString += char

    def __repr__(self):
        s = "< [{}]({}) >".format(self.contents, self.tokens)
        return s

class Code(object):
    def __init__(self, startIndex, closeIndex, closeTagIndex, code, workingStr = None):
        self.startIndex = startIndex
        self.closeIndex = closeIndex
        self.startCode = closeIndex + 1
        self.closeCode = closeTagIndex
        self.code = code
        self.string = workingStr
        self.contents = None

    @property
    def isCode(self):
        return True

    def getCutIndices(self):
        return [(self.startIndex, self.startIndex + 1), (self.closeIndex, self.closeCode + 1)]

    def __repr__(self):
        s = "[{},{}]({})".format(self.startIndex, self.closeIndex, self.code).replace('\n','').replace('\r','')
        return '<<' + s +'>>'

    def __eq__(self, other):
        if self.startIndex == other.startIndex and self.closeIndex == other.closeIndex and self.code == other.code:
            return True
        else:
            return False

class contextCode(Code):
    pass

class contentCode(Code):
    pass

class metaCode(Code):
    pass

codeTypes = {
    contextChar : contextCode,
    contentChar : contentCode,
    metaChar : metaCode,
}

def readCodes(codeStr):
    codes = codeStr.split(' ')
    retCodes = []
    for code in codes:
        if len(code) > 1 and code[0] in codeTypes:
            retCodes.append((code[0], code[1:]))
    return retCodes

def makeCode(startIndex, closeIndex, closeTagIndex, codeStr, workingStr = None):
    validCodes = readCodes(codeStr)
    retCodes = []
    for codeChar, code in validCodes:
        retCodes.append(codeTypes[codeChar](startIndex, closeIndex, closeTagIndex, code, workingStr))
    return retCodes
