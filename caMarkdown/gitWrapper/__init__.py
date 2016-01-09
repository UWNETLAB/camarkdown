from ..caExceptions import GitException

try:
    from .gitPythonStuff import *
    print("***DEBUG***: Using gitPython")
except (ImportError, AttributeError):
    try:
        from .dulwichStuff import *
        print("***DEBUG***: Using dulwich")
    except (ImportError, AttributeError):
        raise GitException("You need to have gitPython or dulwich installed to use caMarkdown.")
