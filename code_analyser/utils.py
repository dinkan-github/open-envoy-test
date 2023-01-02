from enum import Enum


class LineType(Enum):
    BLANK = 'blank'
    SINGLE_COMMENT = 'single_comment'
    MULTI_COMMENT = 'multi_comment'
    CODE = 'code'
    IMPORT_STATEMENT = 'import_statement'
    VAR_DECLARATION = 'var_declaration'


class FileType(Enum):
    DIRECTORY = "directory"
    FILE = "file"


class AnalyzerSupportedLanguages(Enum):
    JAVA = "java"
    PYTHON = "python"

