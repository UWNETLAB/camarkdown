class Code(object):
    def __init__(self, targetString, startIndex):
        self.startIndex = startIndex
        self.closeIndex = None
        self.startCode = None
        self.closeCode = None
        self.codes = None
        self.string = targetString
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
        self.codes = contents

    def setContents(self, contString):
        self.contents = string

    def getCutIndices(self):
        return [(self.startIndex, self.startIndex + 1), (self.closeIndex, self.closeCode + 1)]

    def __repr__(self):
        return ("[{}]({})".format(self.string[self.startIndex + 1:self.closeIndex], self.codes))
