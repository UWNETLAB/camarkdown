import pathlib

confName =  "configuration.py"

defaultConf = """#Default Conf
""".strip()

def makeConf(targetDir):
    """Makes conf file in the current working dir"""
    with open(str(pathlib.Path(targetDir, confName)), 'x') as target:
        target.write(defaultConf)
