import pathlib

from .gitWrappers import containsGitRepo
from .caExceptions import UninitializedDirectory

def findTopDir(startPath):
    """Finds the first directory (including startPath) above startPath that is a git repo
    """
    if not isinstance(startPath, pathlib.Path):
        startPath = pathlib.Path(startPath)
    workingpath = startPath.resolve()
    if not workingpath.is_dir():
        workingpath = workingpath.parent()
    while workingpath.parent != workingpath:
        if containsGitRepo(workingpath):
            return workingpath
        else:
            workingpath = workingpath.parent
    raise UninitializedDirectory("{} is not a caMarkdown directory and none of its parents are either.".format(startPath))
