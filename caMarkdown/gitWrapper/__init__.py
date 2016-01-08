from ..caExceptions import GitException

try:
    from .gitPythonStuff import *
    print("Using gitPython")
except (ImportError, AttributeError):
    try:
        from .dulwichStuff import *
        print("Using dulwich")
    except (ImportError, AttributeError):
        raise GitException("You need to have gitPython or dulwich installed to use caMarkdown.")
