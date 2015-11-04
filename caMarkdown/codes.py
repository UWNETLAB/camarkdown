from .caExceptions import CodeParserException

contextChar = '@'
contentChar = '$'
metaChar = '^'

def lineAndIndexCounter(targtString):
    sIter = enumerate(targtString.__iter__())
    lineCount = 1
    while True:
        i, char = next(sIter)
        if char == '\n':
            lineCount += 1
        yield lineCount, i, char

class parseTree(object):
    def __init__(self, targetString):
        sIter = lineAndIndexCounter(targetString)
        self.topNode = Node(sIter, 0, -1, '')
        self.tagSegments = self.topNode.tagSections
        tmpTagDict = {}
        for seg in self.tagSegments:
            try:
                tmpTagDict[seg.tag].append(seg)
            except KeyError:
                tmpTagDict[seg.tag] = [seg]
        self._tags = {tag : Tag(seg, tag) for tag, seg in tmpTagDict.items()}


class Node(object):
    def __init__(self, sIter, startLine, startIndex, startCode):
        if startCode == '[':
            self.code = True
            self._raw = ''
        else:
            self.code = False
            self._raw = startCode
        self.tokens = None
        self.contents = []
        self.line = startLine
        self.index = startIndex
        self._children = None
        self._containedSections = None
        self._tagSections = None
        self._codes = None

        stopIter = False
        inBraces = False
        currentString = ''
        currentIndex = 0
        currentLine = 1
        freshString = True

        while not stopIter:
            try:
                line, i, char = next(sIter)
                if not inBraces:
                    self._raw += char
                if freshString:
                    currentLine, currentIndex, currentString = line, i, ''
            except StopIteration:
                if inBraces:
                    currentString += '](' + self.tokens
                self.contents.append((currentLine, currentIndex, currentString))
                self.code = False
                stopIter = True
            else:
                if inBraces:
                    if char == ')':
                        stopIter = True
                    else:
                        self.tokens += char
                elif char == '[':
                    self.contents.append((currentLine, currentIndex, currentString))
                    self._raw = self._raw[:-1]
                    innerCode = Node(sIter, line, i, char)
                    self._raw += innerCode.raw
                    self.contents.append(innerCode)
                    freshString = True
                elif char == ']' and self.code:
                    try:
                        line, i, char = next(sIter)
                        self._raw += char
                    except StopIteration:
                        stopIter = True
                    else:
                        if char == '(':
                            self.tokens = ''
                            inBraces = True
                            self.contents.append((currentLine, currentIndex, currentString))
                            self._raw = self._raw[:-2]
                        elif char == '[':
                            self.contents.append((currentLine, currentIndex, currentString))
                            innerCode = Node(sIter, line, i, char)
                            self._raw += innerCode.raw
                            self.contents.append(innerCode)
                            self.code = False
                            stopIter = True
                        else:
                            currentString += ']' + char
                            self.contents.append((currentLine, currentIndex, currentString))
                            stopIter = True
                            self.code = False
                else:
                    currentString += char

    @property
    def raw(self):
        #TODO Consider how to handle this
        return self._raw

    @property
    def children(self):
        if self._children is None:
            children = []
            for val in self.contents:
                if isinstance(val, tuple):
                    pass
                elif isinstance(val, Node):
                    children.append(val)
                else:
                    raise CodeParserException("Node {} contains a non-Node, non-string object: {}".format(self, val))
            self._children = children
        return self._children

    @property
    def containedSections(self):
        if self._containedSections is None:
            self._containedSections = self.codes
            for child in self.children:
                self._containedSections += child.codes
        return self._containedSections

    @property
    def tagSections(self):
        if self._tagSections is None:
            self._tagSections = self.codes
            for c in self.children:
                self._tagSections += c.tagSections
        return self._tagSections


    @property
    def codes(self):
        def readCodes(codeStr):
            codes = codeStr.split(' ')
            retCodes = []
            for code in codes:
                if len(code) > 1 and code[0] in codeTypes:
                    retCodes.append((code[0], code))
            return retCodes

        if self._codes is None:
            self._codes = []
            if self.code:
                tagStrings = readCodes(self.tokens)
                for codeChar, code in tagStrings:
                    self._codes.append(codeTypes[codeChar](self.contents, code, self.line, self.index, self.raw))
        return self._codes

    def __repr__(self):
        if self.code:
            s = "< Node [{}]({}) >".format(len(self._raw), self.tokens)
        else:
            s = "< Node [{}] >".format(len(self._raw))
        return s

class CodeSection(object):
    def __init__(self, contents, tag, startLine, startIndex, startRaw):
        self.contents = contents
        self.tag = tag
        self.line = startLine
        self.index = startIndex
        self._raw = startRaw
        self._children = None

    def __repr__(self):
        s = "< CodeSection [{}]({}) >".format(len(self._raw), self.tag)
        return s

    def __hash__(self):
        return hash(self.raw + self.tag + str(self.index))

    def __len__(self):
        return len(self.raw)

    def __contains__(self, tag):
        for c in self.children:
            if c.tag == tag:
                return True
        return False

    def __getitem__(self, tag):
        retTags = []
        for c in self.children:
            if c.tag == tag:
                retTags.append(c)
        return retTags

    @property
    def raw(self):
        return self._raw

    @property
    def children(self):
        if self._children is None:
            children = []
            for val in self.contents:
                if isinstance(val, tuple):
                    pass
                elif isinstance(val, Node):
                    children.append(val)
                else:
                    raise CodeParserException("Node {} contains a non-Node, non-string object: {}".format(self, val))
            self._children = children
        return self._children

class ContextCodeSection(CodeSection):
    pass

class ContentCodeSection(CodeSection):
    pass

class MetaCodeSection(CodeSection):
    pass

codeTypes = {
    contextChar : ContextCodeSection,
    contentChar : ContentCodeSection,
    metaChar : MetaCodeSection,
}

class Tag(object):
    def __init__(self, sections, tag):
        for s in sections:
            if s.tag != tag:
                raise CodeParserException("Tag objects can ony be made from CodeSections with the same tag. A tag of {} was found when {} was expected".format(s.tag, tag))
        self.sections = sections
        self._containedTags = None
        self._containedSections = None
        self._raw = None

    @property
    def raw(self):
        if self._raw is None:
            self._raw = []
            for sec in self.sections:
                self._raw.append(sec.raw)
        return self._raw


    @property
    def containedSections(self):
        if self._containedSections is None:
            self._containedSections = []
            for sec in self.sections:
                for seg in [node.containedSections for node in sec.children]:
                    self._containedSections += seg
        return self._containedSections

    @property
    def containedTags(self):
        if self._containedTags is None:
            self._containedTags = []
            for sec in self.containedSections:
                if sec.tag not in self._containedTags:
                    self._containedTags.append(sec.tag)
        return self._containedTags
