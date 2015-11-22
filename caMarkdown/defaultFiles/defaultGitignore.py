import pathlib

gitignoreName =  ".gitignore"

defaultGitignore = "#Put the files you want git and caMarkdown to not track here:\n"


def makeGitignore(targetDir):
    """Makes .gitignore in the current working dir"""
    with open(str(pathlib.Path(targetDir, gitignoreName)), 'x') as target:
        target.write(defaultGitignore)
