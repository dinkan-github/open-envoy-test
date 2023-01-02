import pytest

from code_analyser.java_analyser import JavaCodeAnalyser


@pytest.fixture
def java():
    return JavaCodeAnalyser()


def test_blank_line_detection(java):
    assert java.blank().match('   ')
    assert not java.blank().match('import java.util.List')


def test_single_comment_line_detection(java):
    assert java.single_comment().match('   // this is a single-line comment')
    assert not java.single_comment().match('/* this is a multi-line comment */')


def test_multi_comment_line_detection(java):
    assert java.multi_comment().match('   /* this is a multi-line comment')
    assert java.multi_comment().match('   */ this is the end of a multi-line comment \n int a = 12; \n */')
    assert not java.multi_comment().match('// this is a single-line comment')


def test_import_statement_detection(java):
    assert java.import_statement().match('import java.util.List')
    assert not java.import_statement().match('class MyClass {')


def test_var_declaration_detection(java):
    assert java.var_declaration().match('int num = 10;')
    assert java.var_declaration().match('double d = 3.14;')
    assert not java.var_declaration().match('System.out.println("Hello, world!");')
