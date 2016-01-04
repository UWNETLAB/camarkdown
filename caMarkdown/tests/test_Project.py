import unittest
import tempfile
import os.path
import shutil
import pathlib

import caMarkdown

from .helpers import makeTestDir

testingFilesDir = os.path.join(os.path.dirname(__file__), 'womenInComp')

tempDirName = 'tempTestingDir'

class Test_Project(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        makeTestDir(tempDirName, testingFilesDir)

    def setUp(self):
        pass

    def test_init(self):
        P = caMarkdown.Project(tempDirName)
        P.initializeDir()
        self.assertEqual(P.path, pathlib.Path(tempDirName).resolve())

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(tempDirName)
