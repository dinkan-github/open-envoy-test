import pytest

from code_analyser.python_analyser import PythonCodeAnalyser


@pytest.fixture
def python():
    return PythonCodeAnalyser()


def test_blank_regex(python):
    blank_regex = python.blank()
    assert blank_regex.match('   ') is not None
    assert blank_regex.match('\t') is not None
    assert blank_regex.match('') is not None
    assert blank_regex.match('  # comment') is None
    assert blank_regex.match('var = 123') is None


def test_single_comment_regex(python):
    single_comment_regex = python.single_comment()
    assert single_comment_regex.match('# comment') is not None
    assert single_comment_regex.match('   # comment') is not None
    assert single_comment_regex.match('#') is not None
    assert single_comment_regex.match('') is None
    assert single_comment_regex.match('var = 123') is None
    assert single_comment_regex.match('""" multi-line comment """') is None


def test_multi_comment_regex(python):
    multi_comment_regex = python.multi_comment()
    assert multi_comment_regex.match('""" multi-line comment """') is not None
    assert multi_comment_regex.match('   """ multi-line comment """') is not None
    assert multi_comment_regex.match('"""') is not None
    assert multi_comment_regex.match('') is None
    assert multi_comment_regex.match('var = 123') is None
    assert multi_comment_regex.match('# comment') is None


def test_import_statement_regex(python):
    import_statement_regex = python.import_statement()
    assert import_statement_regex.match('import module') is not None
    assert import_statement_regex.match('from package import module') is not None
    assert import_statement_regex.match('   import module') is not None
    assert import_statement_regex.match('   from package import module') is not None
    assert import_statement_regex.match('') is None
    assert import_statement_regex.match('var = 123') is None
    assert import_statement_regex.match('""" multi-line comment """') is None
    assert import_statement_regex.match('# comment') is None


def test_var_declaration_regex(python):
    var_declaration_regex = python.var_declaration()
    assert var_declaration_regex.match('var = 123') is not None
    assert var_declaration_regex.match('   var = 123') is not None
    assert var_declaration_regex.match('var =') is not None
    assert var_declaration_regex.match('') is None
    assert var_declaration_regex.match('import module') is None
    assert var_declaration_regex.match('""" multi-line comment """') is None
    assert var_declaration_regex.match('# comment') is None
