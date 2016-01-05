#IN PROGRESS
import dulwich.repo
import dulwich.objects
import dulwich.errors

from .caExceptions import GitException, GitRepositoryMissing

def containsGitRepo(targetDir):
    """Checks if targetDir can be initialized as a git repo"""
    try:
        openRepo(targetDir)
    except GitRepositoryMissing:
        return False
    else:
        return True

def openRepo(targetDir):
    """Opens targetDir as a dulwich repo"""
    try:
        return dulwich.repo.Repo(str(targetDir))
    except dulwich.errors.NotGitRepository:
        raise GitRepositoryMissing("No git repo found at {}".format(targetDir))

def init(targetDir):
    """initializes and retuns targetDir as a dulwich repo
    """
    return dulwich.repo.Repo.init(str(targetDir))

def commit(fileNames, message):
    blobs = []
    for fname in fileNames:
        with open(fname, 'r') as f:
            blobs.append(dulwich.objects.Blob.from_file(f))
    tree = dulwich.objects.Tree()
    commit = dulwich.objects.Commit()
    commit.tree = tree.id
