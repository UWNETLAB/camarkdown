from .parser import *

def reload():
    import sys
    import importlib
    sys.modules['caMarkdown'] = importlib.reload(sys.modules['caMarkdown'])
    print("caMarkdown has been reloaded")
