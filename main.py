import logging
import os

from code_analyser.base import AbstractCodeAnalyser
from code_analyser.java_analyser import JavaCodeAnalyser
from code_analyser.python_analyser import PythonCodeAnalyser
from code_analyser.utils import AnalyzerSupportedLanguages, FileType

analyser_class_mapping = {
    AnalyzerSupportedLanguages.JAVA.value: JavaCodeAnalyser,
    AnalyzerSupportedLanguages.PYTHON.value: PythonCodeAnalyser
}

analyser_file_extn_mapping = {
    'java': JavaCodeAnalyser,
    'py': PythonCodeAnalyser
}

if __name__ == '__main__':
    path = input("Enter the directory or file path: ")

    if os.path.isdir(path):
        selected_option = input("Enter the language <java, python>: ").lower().strip()
        supported_languages = [e.value for e in AnalyzerSupportedLanguages]
        while selected_option not in supported_languages:
            print("Invalid option. Please try again.")
            selected_option = input("Enter the language <java, python>: ").lower().strip()
        parser: AbstractCodeAnalyser = analyser_class_mapping[selected_option](path=path, type=FileType.DIRECTORY)
        parser.get_breakdown()
    elif os.path.isfile(path):
        extension = path.split('.')[-1]
        if analyser_file_extn_mapping.get(extension):
            parser: AbstractCodeAnalyser = analyser_file_extn_mapping[extension](path=path)
            parser.get_breakdown()
        else:
            logging.error(f"not implemented for files with {extension} extension. "
                          f"Available integrations: .java, .py (Java and Python)")
    else:
        logging.error("The path is neither a directory nor a file.")
