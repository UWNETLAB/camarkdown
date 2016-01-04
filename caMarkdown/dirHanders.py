import os
import shutil
import pathlib

import dulwich.repo
import dulwich.errors

from .caExceptions import UninitializedDirectory

def findTopDir(startPath):
    if not isinstance(startPath, pathlib.Path):
        startPath = pathlib.Path(startPath)
    workingpath = startPath.resolve()
    if not workingpath.is_dir():
        workingpath = workingpath.parent()
    while workingpath.parent != workingpath:
        try:
            workingpath.glob('.git').__next__()
        except StopIteration:
            workingpath = workingpath.parent
        else:
            return workingpath
    raise UninitializedDirectory("{} is not a caMarkdown directory and none of its parents are either.".format(startPath))
