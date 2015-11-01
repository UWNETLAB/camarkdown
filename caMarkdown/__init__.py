from .parser import tokenizer, getCodes, tokenizer2, getCodes2
from .tests.testGen import makeTestFile
from .dirHanders import makeProjectDir

import os.path

def _reload():
    """This is for develop purposes only do not use otherwise. _reload() is not to be trusted as it is evil and will create zombies (also it sometimes doesn't work)."""
    import sys
    import importlib
    for i in range(3):
        for modName in sys.modules.keys():
            if "caMarkdown" == modName[:10]:
                sys.modules[modName] = importlib.reload(sys.modules[modName])
    print("caMarkdown has been reloaded, Zombies have risen")
