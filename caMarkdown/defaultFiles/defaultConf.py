confName =  "configuration.py"

defaultConf = """#Default Conf
""".strip()

def makeConf():
    """Makes conf file in the current working dir"""
    with open(confName, 'x') as target:
        target.write(defaultConf)
