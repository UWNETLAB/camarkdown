codeBookName = "codebook.md"

defaultCookbook="""
# Target Files

# Context Codes


# Content Codes


#Meta Codes
""".strip()

def makeCodeBook():
    """Makes code book in the current working dir"""
    with open(codeBookName, 'x') as target:
        target.write(defaultCookbook)
