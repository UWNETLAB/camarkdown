import unittest
import os.path
import shutil
import pathlib

import caMarkdown

from .helpers import makeTestDir

from ..defaultFiles.defaultCodebook import codeBookName
from ..defaultFiles.defaultConf import confName
from ..defaultFiles.defaultGitignore import gitignoreName
from ..defaultFiles.defaultCaignore import caIgnoreName

testingFilesDir = os.path.join(os.path.dirname(__file__), 'womenInComp')

tempDirName = 'tempTestingDir'

class Test_Project(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        makeTestDir(tempDirName, testingFilesDir)

    def setUp(self):
        self.P = caMarkdown.Project(tempDirName)
        self.P.initializeDir()

    def test_creation(self):
        self.assertEqual(self.P.path, pathlib.Path(tempDirName).resolve())
        self.assertIsInstance(pathlib.Path(self.P.path, codeBookName).resolve(), pathlib.Path)
        self.assertIsInstance(pathlib.Path(self.P.path, confName).resolve(), pathlib.Path)
        self.assertIsInstance(pathlib.Path(self.P.path, gitignoreName).resolve(), pathlib.Path)
        self.assertIsInstance(pathlib.Path(self.P.path, caIgnoreName).resolve(), pathlib.Path)

    def tearDown(self):
        self.P.delete(force = True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(tempDirName)
