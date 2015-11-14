class AddingException(Exception):
    pass

class CodeParserException(Exception):
    pass

class UninitializedDirectory(Exception):
    pass

class ProjectException(Exception):
    pass

class ProjectDirectoryMissing(ProjectException):
    pass

class ProjectMissingFiles(ProjectException):
    pass
