import re

from code_analyser.base import AbstractCodeAnalyser
from code_analyser.utils import FileType


class JavaCodeAnalyser(AbstractCodeAnalyser):
    def __init__(self, path=None, type: FileType = FileType.FILE):
        super().__init__(path, type)

    def blank(self) -> re.Pattern:
        return re.compile(r'^\s*$')

    def single_comment(self) -> re.Pattern:
        return re.compile(r'^\s*//')

    def multi_comment(self) -> re.Pattern:
        return re.compile(r'^\s*/\*|^\s*\*/')

    def import_statement(self) -> re.Pattern:
        return re.compile(r'^\s*import')

    def var_declaration(self) -> re.Pattern:
        return re.compile(r'^\s*(boolean|byte|char|short|int|long|float|double)\s*\w+')
