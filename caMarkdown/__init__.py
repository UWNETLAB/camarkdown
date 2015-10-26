from .parser import tokenizer, getCodes
from .tests.testGen import makeTestFile

import os.path

def _reload():
    """This is for develop purposes only do not use otherwise.
    _reload() is not to be trusted as it is evil and will create zombies"""
    import sys
    import importlib
    for modName in sys.modules.keys():
        if "caMarkdown" == modName[:10]:
            sys.modules[modName] = importlib.reload(sys.modules[modName])
    print("caMarkdown has been reloaded, Zombies have risen")

def test():
    loc = os.path.dirname(__file__) + "/tests"
    fileParse(loc + "/RecordTarget.md", loc + "/RecordMaster.md")
