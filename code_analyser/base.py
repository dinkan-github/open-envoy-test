import logging
import os

from code_analyser.utils import FileType, LineType


class AbstractCodeAnalyser(object):
    def __init__(self, path=None, type: FileType = FileType.FILE):
        self.__inside_multiline_comment = False
        self.blank_lines = 0
        self.single_comment_lines = 0
        self.multi_comment_lines = 0
        self.code_lines = 0
        self.import_lines = 0
        self.var_declaration_lines = 0
        self.__file_path = path
        self.__type = type

    def blank(self):
        raise NotImplementedError

    def single_comment(self):
        raise NotImplementedError

    def multi_comment(self):
        raise NotImplementedError

    def import_statement(self):
        raise NotImplementedError

    def var_declaration(self):
        raise NotImplementedError

    def _get_line_type(self, line):
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
        if not self.__file_path:
            return logging.error(f"required a file_path")
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
    def _get_lines(file_path):
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
