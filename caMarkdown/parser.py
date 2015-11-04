from .codes import Node, lineAndIndexCounter, parseTree



def getParseTree(targetString):
    sIter = lineAndIndexCounter(targetString)
    return Node(sIter, 0, -1, '')

def getTags(targetString):
    tree = parseTree(targetString)
    return tree
