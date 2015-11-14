caIgnoreName =  ".camdignore"

defaultCAignore = """#Put the files you do not want caMarkdown to track here:
#By default only those ending in .md or .markdown are tracked

*

!*.md
!*.markdown
"""


def makeCAignore():
    """Makes .camdignore in the current working dir"""
    with open(caIgnoreName, 'x') as target:
        target.write(defaultCAignore)
