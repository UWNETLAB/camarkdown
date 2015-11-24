from ..codes import contextChar, contentChar, metaChar

import yaml

import pathlib

codeBookName = "codebook.yaml"



codebookFileHeader = "Files"
codebookContentHeader = "ContextCodes"
codebookContextHeader = "ContentCodes"
codebookMetaHeader = "MetaCodes"
codebookHeaders = [codebookContentHeader, codebookContextHeader, codebookMetaHeader, codebookFileHeader]

charHeaderMap = {
contextChar : codebookContextHeader,
contentChar : codebookContentHeader,
metaChar : codebookMetaHeader,
}

headerCharMap = {value : key for key, value in charHeaderMap.items()}

def makeCodeBook(targetDir, headers = codebookHeaders):
    """Makes code book in the current working dir"""
    with open(str(pathlib.Path(targetDir, codeBookName)), 'x') as target:
        target.write("{}:\n    \n    \n".format(':\n    \n    \n'.join(headers)))
