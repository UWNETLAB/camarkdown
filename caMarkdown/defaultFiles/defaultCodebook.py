from ..codes import contextChar, contentChar, metaChar

codeBookName = "codebook.md"

codebookFileHeader = "# Target Files\n"
codebookContentHeader = "# Context Codes\n"
codebookContextHeader = "# Content Codes\n"
codebookMetaHeader = "# Meta Codes\n"
codebookHeaders = [codebookFileHeader, codebookContentHeader, codebookContextHeader, codebookMetaHeader]

headerCharMap = {
contextChar : codebookContextHeader,
contentChar : codebookContentHeader,
metaChar : codebookMetaHeader,
}

def makeCodeBook(headers = codebookHeaders):
    """Makes code book in the current working dir"""
    with open(codeBookName, 'x') as target:
        print(headers)
        target.write("{}\n\n".format('\n\n'.join(headers)))
