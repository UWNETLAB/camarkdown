class caMarkdownException(Exception):
    """The base class of all excptions for caMarkdown"""
    pass

class AddingException(caMarkdownException):
    pass

class CodeParserException(caMarkdownException):
    pass

class UninitializedDirectory(caMarkdownException):
    pass

class ProjectException(caMarkdownException):
    pass

class ProjectTypeError(ProjectException):
    pass

class ProjectDirectoryMissing(ProjectException):
    pass

class ProjectMissingFiles(ProjectException):
    pass

class ProjectFileError(ProjectException):
    pass

class ProjectCodeError(ProjectException):
    pass

class ProjectGitError(ProjectFileError):
    pass

class ProjectReservedFileError(ProjectFileError):
    pass

class CodeBookException(caMarkdownException):
    pass

class TestError(caMarkdownException):
    pass

class GitException(caMarkdownException):
    pass

class GitRepositoryMissing(GitException):
    pass
