import os.path
from ..parser import *

loc = os.path.dirname(__file__)
def test():
    fileParse(loc + "/RecordTarget.md", loc + "/RecordMaster.md")
