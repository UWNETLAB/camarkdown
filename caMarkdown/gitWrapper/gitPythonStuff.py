import git

from ..caExceptions import GitException, GitRepositoryMissing

__all__ = ['containsGitRepo', 'openRepo', 'init']

def containsGitRepo(targetDir):
    """Checks if targetDir can be initialized as a git repo"""
    try:
        openRepo(targetDir)
    except GitRepositoryMissing:
        return False
    else:
        return True

def openRepo(targetDir):
    """Opens targetDir as a gitPython repo"""
    try:
        return git.Repo(str(targetDir), search_parent_directories = False)
    except git.exc.InvalidGitRepositoryError:
        raise GitRepositoryMissing("No git repo found at {}".format(targetDir))

def init(targetDir):
    """initializes and retuns targetDir as a gitPython repo
    """
    return git.Repo.init(str(targetDir))
