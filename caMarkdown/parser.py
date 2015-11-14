from .codes import Node, lineAndIndexCounter, parseTree

def getParseTree(targetString):
    return parseTree(targetString)

def getTags(targetString):
    tree = parseTree(targetString)
    return tree.tags
