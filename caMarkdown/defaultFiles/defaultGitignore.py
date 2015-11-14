gitignoreName =  ".gitignore"

defaultGitignore = "#Put the files you want git and caMarkdown to not track here:\n"


def makeGitignore():
    """Makes .gitignore in the current working dir"""
    with open(gitignoreName, 'x') as target:
        target.write(defaultGitignore)
