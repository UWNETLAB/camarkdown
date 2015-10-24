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

    def closeText(self, closeIndex):
        self.closeIndex = closeIndex

    def startBrace(self, startCode):
        self.startCode = startCode

    def closeBrace(self, closeCode, contents = None):
        self.closeCode = closeCode
        self.code = contents

    def setContents(self, contString):
        self.contents = string

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

codeTypes = {
    '^' : Code
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
