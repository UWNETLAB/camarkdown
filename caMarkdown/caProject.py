from .defaultFiles.defaultCodebook import makeCodeBook, codeBookName
from .defaultFiles.defaultConf import makeConf, confName
from .defaultFiles.defaultGitignore import makeGitignore, gitignoreName
from .defaultFiles.defaultCaignore import makeCAignore, caIgnoreName

from .caExceptions import AddingException, UninitializedDirectory, ProjectDirectoryMissing, ProjectMissingFiles

import dulwich.repo
import dulwich.errors

import pathlib
import os.path

class Project(object):
    def __init__(self, dirName, fresh = False):
        self.Path = pathlib.Path(os.path.expanduser(os.path.expandvars(dirName))).resolve()
        self.Repo = None
        if fresh:
            self.initializeDir()
        self.reopen()

    def reopen(self):
        try:
            os.chdir(str(self.Path))
        except OSError:
            raise ProjectDirectoryMissing("{} could not be accessed, does it exist and do you have permission to acccess it?".format(self.Path))
        try:
            self.Repo = dulwich.repo.Repo('.')
        except dulwich.errors.NotGitRepository:
            raise ProjectMissingFiles("{} is not a git repo. It cannot be reopen as a caMarkdown repo".format(str(self.Path)))
        for name in [confName, codeBookName, gitignoreName, caIgnoreName]:
            if not pathlib.Path(name).exists():
                raise ProjectMissingFiles("{} is missing, this is not a caMarkdown repo.".format(name))

    def initializeDir(self):
        try:
            self.Path.mkdir(parents = True)
        except FileExistsError:
            pass
        try:
            os.chdir(str(self.Path))
        except OSError:
            raise ProjectDirectoryMissing("{} could not be accessed, do you have permission to acccess it?".format(str(self.Path)))
        #Create all the missing files and directories
        try:
            self.Repo = dulwich.repo.Repo('.')
        except dulwich.errors.NotGitRepository:
            self.Repo = dulwich.repo.Repo.init('.')
        try:
            makeCodeBook()
        except FileExistsError:
            pass
        try:
            makeConf()
        except FileExistsError:
            pass
        try:
            makeGitignore()
        except FileExistsError:
            pass
        try:
            makeCAignore()
        except FileExistsError:
            pass
