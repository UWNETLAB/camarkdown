from .caExceptions import CodeParserException

contextChar = '@'
contentChar = '$'
metaChar = '^'

class Node(object):
    def __init__(self, sIter, codeStart):
        if codeStart == '[':
            self.code = True
        else:
            self.code = False
        self.tokens = None
        self.contents = []
        self._raw = codeStart
        self._children = None

        stopIter = False
        inBraces = False
        currentString = ''

        while not stopIter:
            try:
                char = next(sIter)
                self._raw += char
            except StopIteration:
                if inBraces:
                    currentString += '](' + self.tokens
                self.contents.append(currentString)
                self.code = False
                stopIter = True
            else:
                if inBraces:
                    if char == ')':
                        stopIter = True
                    else:
                        self.tokens += char
                elif char == '[':
                    self.contents.append(currentString)
                    self._raw = self._raw[:-1]
                    innerCode = Node(sIter, char)
                    self.contents.append(innerCode)
                elif char == ']' and self.code:
                    try:
                        char = next(sIter)
                        self._raw += char
                    except StopIteration:
                        stopIter = True
                    else:
                        if char == '(':
                            self.tokens = ''
                            inBraces = True
                            self.contents.append(currentString)
                        elif char == '[':
                            self.contents.append(Code2(sIter))
                            self.code = False
                            stopIter = True
                        else:
                            currentString += ']' + char
                            self.contents.append(currentString)
                            stopIter = True
                            self.code = False
                else:
                    currentString += char

    @property
    def raw(self):
        if len(self._raw) < 2:
            for child in self.contents:
                self._raw += child.raw
        return self._raw



    @property
    def children(self):
        if self._children is None:
            children = []
            for val in self.contents:
                if isinstance(val, Node):
                    children.append(val)
                else:
                    raise CodeParserException("Node {} contains a non-Node, non-string object: {}".format(self, val))
            self._children = children
        return self._children

    def __repr__(self):
        if self.code:
            s = "< [{}]({}) >".format(len(self._raw), self.tokens)
        else:
            s = "< [{}] >".format(len(self._raw))
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
