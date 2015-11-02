from .codes import Code, Node

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
