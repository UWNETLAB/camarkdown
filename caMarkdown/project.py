from .defaultFiles.defaultCodebook import makeCodeBook, codeBookName, codebookHeaders, headerCharMap
from .defaultFiles.defaultConf import makeConf, confName
from .defaultFiles.defaultGitignore import makeGitignore, gitignoreName
from .defaultFiles.defaultCaignore import makeCAignore, caIgnoreName

from .codes import parseTree, codeTypes, makeCode
from .caExceptions import AddingException, UninitializedDirectory, ProjectDirectoryMissing, ProjectMissingFiles, ProjectException, ProjectTypeError, CodeBookException, ProjectFileError, ProjectCodeError

import dulwich.repo
import dulwich.errors

import pathlib
import os.path
import fnmatch
import re
import collections

class Project(object):
    def __init__(self, dirName):
        if isinstance(dirName, pathlib.Path):
            self.path = dirName.resolve()
        elif isinstance(dirName, str):
            self.path = pathlib.Path(os.path.expanduser(os.path.expandvars(dirName))).resolve()
        else:
            raise ProjectTypeError("Objects of type: '{}' are not a valid input for inilizing a project object, the provided object was: {}".format(type(dirName), dirName))
        self.Repo = None
        self.error = None
        self.bad = False

        self._code = None

        try:
            self.openDir()
        except ProjectException as e:
            self.error = e
            self.bad = True

    def _openCAIgnore(self, mode = 'r'):
        try:
            f = open(str(pathlib.Path(self.path, pathlib.Path(caIgnoreName))), mode = mode)
        except FileNotFoundError:
            raise ProjectMissingFiles("{} missing".format(caIgnoreName))
        else:
            return f

    def _openGitIgnore(self, mode = 'r'):
        try:
            f = open(str(pathlib.Path(self.path, pathlib.Path(gitignoreName))), mode = mode)
        except FileNotFoundError:
            raise ProjectMissingFiles("{} missing".format(gitignoreName))
        else:
            return f

    def _openCodebook(self, mode = 'r'):
        try:
            f = open(str(pathlib.Path(self.path, pathlib.Path(codeBookName))), mode = mode)
        except FileNotFoundError:
            raise ProjectMissingFiles("{} missing".format(codeBookName))
        else:
            return f

    def openDir(self):
        try:
            self.Repo = dulwich.repo.Repo(str(self.path))
        except dulwich.errors.NotGitRepository:
            raise ProjectMissingFiles("{} is not a git repo. It cannot be reopen as a caMarkdown repo".format(str(self.path)))
        for name in [confName, codeBookName, gitignoreName, caIgnoreName]:
            if not pathlib.Path(self.path, name).exists():
                raise ProjectMissingFiles("{} is missing, this is not a caMarkdown repo.".format(name))

    def initializeDir(self):
        try:
            self.path.mkdir(parents = True)
        except FileExistsError:
            pass
        #Create all the missing files and directories
        try:
            self.Repo = dulwich.repo.Repo(str(self.path))
        except dulwich.errors.NotGitRepository:
            self.Repo = dulwich.repo.Repo.init(str(self.path))
        try:
            makeCodeBook(self.path)
        except FileExistsError:
            pass
        try:
            makeConf(self.path)
        except FileExistsError:
            pass
        try:
            makeGitignore(self.path)
        except FileExistsError:
            pass
        try:
            makeCAignore(self.path)
        except FileExistsError:
            pass

    def getGitIgnoreRules(self):
        """Does not work quite right
        """
        f = self._openGitIgnore()
        rules = []
        for ruleString in (rule.split('#')[0].rstrip() for rule in f.readlines()):
            if len(ruleString) > 0:
                rules.append(lambda s: not fnmatch.fnmatch(s, ruleString))
        f.close()
        return rules

    def getCAIgnoreRules(self):
        """Does not work quite right
        """
        f = self._openCAIgnore
        rules = []
        for ruleString in (rule.split('#')[0].rstrip() for rule in f.readlines()):
            if len(ruleString) > 0:
                rules.append(lambda s: not fnmatch.fnmatch(s, ruleString))
        f.close()
        return rules

    def addFile(self, targetPath):
        """Appends the codebook with the path to targetPath"""
        if not isinstance(targetPath, pathlib.Path):
            targetPath = pathlib.Path(targetPath)
        try:
            targetPath = targetPath.resolve()
        except FileNotFoundError:
            raise ProjectFileError("'{}' is not an existing file.".format(targetPath))
        if self.path not in targetPath.parents:
            raise ProjectFileError("'{}' is not in the targeted repository '{}'.".format(targetPath, self.path))
        if not targetPath.is_file():
            raise ProjectFileError("'{}' is not a file.".format(targetPath, self.path))
        with self._openCodebook(mode = 'a') as f:
            f.write(str(targetPath.relative_to(self.path)) + '\n')

    def addCode(self, targetCode, description = None):
        if targetCode in self.codes:
            if not self.codes[targetCode].unDocumented:
                raise ProjectCodeError("The code '{}' already exists".format(targetCode))
        if targetCode[0] not in codeTypes:
            raise ProjectCodeError("The code '{}' does not start with the correct character, it cannot be a code.".format(targetCode))
        for char in targetCode:
            if char.isspace():
                raise ProjectCodeError("The code '{}' has a whitespace character, it cannot be a code.".format(targetCode))
        if description and '\n' in description:
            raise ProjectCodeError("The description '{}' has a newline character, it must only be one line long.".format(description))
        with self._openCodebook(mode = 'a') as f:
            if description is None:
                f.write(targetCode + '\n')
            else:
                f.write("{} : {}\n".format(targetCode, description))

    def organizeCodebook(self):
        with self._openCodebook(mode = 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            sections = collections.OrderedDict()
            for header in codebookHeaders:
                sections[header] = []
            currentSection = codebookHeaders[0]
            for line in lines:
                if line.isspace():
                    pass
                elif line in sections:
                    currentSection = line
                elif line.lstrip()[0] == '#':
                    sections[currentSection].append(line)
                elif line.lstrip()[0] not in headerCharMap:
                    sections[codebookHeaders[0]].append(line)
                else:
                    sections[headerCharMap[line.lstrip()[0]]].append(line)
            for sec, secLines in sections.items():
                f.write(sec)
                f.write(''.join(secLines))
                f.write("\n")
            f.truncate()

    def getFiles(self):
        """gets all files from codebook"""
        retPaths =[]
        for fpath in self.readFilesList():
            if fpath.exists():
                retPaths.append(fpath)
        return retPaths

    def getAllTrackedFiles(self):
        """Doesn't actually read the gitignore yet
        Just gets all the files in the project dir, excluding the special ones"""
        rules = self.getGitIgnoreRules()
        def condenseRules(target, ruleLst):
            for rule in ruleLst:
                if rule(str(target)):
                    return True
            return False
        condensedRule = lambda x: condenseRules(x, ruleLst)
        def getFiles(Path, rule):
            retLst = []
            for subPath in (p for p in Path.iterdir() if rule(p)):
                if subPath.is_dir():
                    retLst += getFiles(subPath, rule)
                else:
                    retLst.append(subPath)
            return retLst
        #TODO: Make work
        #return getFiles(self.path, condensedRule)
        return getFiles(self.path, lambda x: x.name[0] != '.' and x.name != 'configuration.py' and x.name != "codebook.md") #Return all nonhidden files

    def parseTree(self):
        files = self.getFiles()
        if len(files) > 0:
            with open(str(files[0]), 'r') as f:
                tree = parseTree(f.read(), files[0].relative_to(self.path))
            for fname in files[1:]:
                with open(str(fname), 'r') as f:
                    tree += parseTree(f.read(), fname.relative_to(self.path))
        else:
            tree = parseTree('')
        return tree

    def readCodebook(self):
        f = self._openCodebook()
        codes = {}
        files = []
        #The tag type [] cannot start with ^ as that results in negation, thus they need to be sorted before the regex sees them
        codeRegex = re.compile(r'^\s*([{}][^:\s]*)((\s*:\s*)(.*))?'.format(''.join(sorted(codeTypes.keys()))))
        for lineNum, line in enumerate(f.readlines()):
            decommentedLine = line.split('#')[0].strip()
            if len(decommentedLine) > 0:
                regResult = re.match(codeRegex, decommentedLine)
                if regResult:
                    codes[regResult.group(1)] = regResult.group(4)
                else:
                    try:
                        files.append(pathlib.Path(self.path, decommentedLine).resolve())
                    except FileNotFoundError:
                        #This should not be accessible
                        raise CodeBookException("Line number {0} of the codebook in {1} does not contain a code, a comment or a parseable file path. The line is:\n{2}".format(lineNum + 1, self.path, line[:-1]))
        f.close()
        return codes, files

    def readCodes(self):
        return self.readCodebook()[0]

    def readFilesList(self):
        return self.readCodebook()[1]

    @property
    def codes(self):
        if self._code is None:
            self._code = self.getCodes()
        return self._code

    def getCodes(self):
        codebookCodes = self.readCodes()
        documentCodes = self.parseTree().tags
        for codeString, comment in codebookCodes.items():
            if codeString in documentCodes:
                documentCodes[codeString].addComment(comment)
            else:
                unUsedCode = makeCode(codeString, comment = comment)
                unUsedCode.unDocumented = False
                documentCodes[codeString] = unUsedCode
        return documentCodes
