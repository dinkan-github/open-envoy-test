import logging
import os
import re
from typing import List

from code_analyser.utils import FileType, LineType


class AbstractCodeAnalyser(object):
    """
    This code defines an abstract base class ``AbstractCodeAnalyser`` for analyzing code files. This class has several
    methods that are meant to be implemented by subclasses to provide regular expressions for identifying different
    types of lines in code files (e.g., blank lines, lines with single-line comments, lines with multi-line comments,
    lines with import statements, and lines with variable declarations).

    This class has several the following instance variables:

    ``blank_lines``: The number of blank lines in the code file.
    ``single_comment_lines``: The number of lines with single-line comments in the code file.
    ``multi_comment_lines``: The number of lines with multi-line comments in the code file.
    ``code_lines``: The number of lines with code in the code file (excluding blank lines, comments, import statements,
    and variable declarations).
    ``import_lines``: The number of lines with import statements in the code file.
    ``var_declaration_lines``: The number of lines with variable declarations in the code file.

    """

    def __init__(self, path=None, type: FileType = FileType.FILE):
        """
        :param path: The path to the code file being analyzed.
        :param type: The type of the file being analyzed (either a file or a directory). Defaults to file
        """
        self.__inside_multiline_comment = False
        self.blank_lines = 0
        self.single_comment_lines = 0
        self.multi_comment_lines = 0
        self.code_lines = 0
        self.import_lines = 0
        self.var_declaration_lines = 0
        self.__file_path = path
        self.__type = type

    def blank(self) -> re.Pattern:
        """
        This method should be implemented by subclasses and should return a regular expression that matches
         blank lines.
        :return: an instance of the re.Pattern class
        """
        raise NotImplementedError

    def single_comment(self) -> re.Pattern:
        """
        This method should be implemented by subclasses and should return a regular expression that matches lines
        with single-line comments.
        :return: an instance of the re.Pattern class
        """
        raise NotImplementedError

    def multi_comment(self) -> re.Pattern:
        """
        This method should be implemented by subclasses and should return a regular expression that matches lines
        with multi-line comments.
        :return: an instance of the re.Pattern class
        """
        raise NotImplementedError

    def import_statement(self) -> re.Pattern:
        """
        This method should be implemented by subclasses and should return a regular expression that matches lines
        with import statements.
        :return: an instance of the re.Pattern class
        """
        raise NotImplementedError

    def var_declaration(self) -> re.Pattern:
        """
         This method should be implemented by subclasses and should return a regular expression that matches
         lines with variable declarations.
        :return: an instance of the re.Pattern class
        """
        raise NotImplementedError

    def _get_line_type(self, line) -> LineType:
        """
        Takes a line of code as input and returns the type of the line. This method
         is used to classify the lines in a code file according to their type.
        :param line: a line of source code
        :return: LineType enum
        """
        if self.__inside_multiline_comment:
            if self.multi_comment().match(line):
                self.__inside_multiline_comment = False
            return LineType.MULTI_COMMENT
        else:
            if self.multi_comment().match(line):
                self.__inside_multiline_comment = True
                return LineType.MULTI_COMMENT

            implemented_methods = [attr for attr in dir(self) if
                                   callable(getattr(self, attr)) and not attr.startswith('_')]
            excluded_methods = ['get_breakdown']
            for method in list(set(implemented_methods) - set(excluded_methods)):
                if getattr(self, method)().match(line):
                    return LineType(method)
        return LineType.CODE

    def get_breakdown(self):
        """
        This method processes a code file (or all the files in a directory) and returns a breakdown of the number
        of lines of each type in the file(s).
        :return:
        """
        if not self.__file_path:
            logging.error(f"required a file_path")
            return
        else:
            if self.__type == FileType.DIRECTORY:
                self._process_directory()
            else:
                self.file_name = self.__file_path.split('/')[-1]
                self._get_file_breakdown(self._get_lines(self.__file_path))

    def _process_directory(self):
        file_list = os.listdir(self.__file_path)

        for file in file_list:
            file_path = os.path.join(self.__file_path, file)
            if os.path.isfile(file_path):
                self.file_name = file
                self._get_file_breakdown(self._get_lines(file_path))
            else:
                # Assuming filepath is a directory (nested)
                analyser: AbstractCodeAnalyser = self.__class__(path=file_path, type=FileType.DIRECTORY)
                analyser.get_breakdown()

    @staticmethod
    def _get_lines(file_path) -> List[str]:
        lines = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line for line in f]
        except UnicodeDecodeError:
            pass
        return lines

    def _get_file_breakdown(self, lines):
        line_types = [self._get_line_type(line) for line in lines]
        self.blank_lines = line_types.count(LineType.BLANK)
        self.single_comment_lines = line_types.count(LineType.SINGLE_COMMENT)
        self.multi_comment_lines = line_types.count(LineType.MULTI_COMMENT)
        self.code_lines = sum([line_types.count(LineType.CODE), line_types.count(LineType.IMPORT_STATEMENT),
                               line_types.count(LineType.VAR_DECLARATION)])
        self.import_lines = line_types.count(LineType.IMPORT_STATEMENT)
        self.var_declaration_lines = line_types.count(LineType.VAR_DECLARATION)
        self.__line_types = line_types

        self._print_results()

    def _print_results(self):
        max_width = max(len('blank_lines'), len('single_comment_lines'), len('multi_comment_lines'),
                        len('code_lines'), len('import_lines'), len('var_declaration_lines'), len('total'))

        print(f"File: {self.file_name}\n")

        print(f"{' ' * (max_width - len('blank_lines'))}blank_lines |"
              f"{' ' * (max_width - len('single_comment_lines'))}single_comment_lines |"
              f"{' ' * (max_width - len('multi_comment_lines'))}multi_comment_lines |"
              f"{' ' * (max_width - len('code_lines'))}code_lines |"
              f"{' ' * (max_width - len('import_lines'))}import_lines |"
              f"{' ' * (max_width - len('var_declaration_lines'))}var_declaration_lines |"
              f"{' ' * (max_width - len('total'))}total |")

        print('-' * (max_width * 7))

        print(f"{' ' * (max_width - len(str(self.blank_lines)))}{self.blank_lines} |"
              f"{' ' * (max_width - len(str(self.single_comment_lines)))}{self.single_comment_lines} |"
              f"{' ' * (max_width - len(str(self.multi_comment_lines)))}{self.multi_comment_lines} |"
              f"{' ' * (max_width - len(str(self.code_lines)))}{self.code_lines} |"
              f"{' ' * (max_width - len(str(self.import_lines)))}{self.import_lines} |"
              f"{' ' * (max_width - len(str(self.var_declaration_lines)))}{self.var_declaration_lines} |"
              f"{' ' * (max_width - len(str(len(self.__line_types))))}{len(self.__line_types)} |\n")
