import pytest

from kurrwa import tokenize, readInput, calculate


@pytest.mark.parametrize("expr,expected", [
    ("1 + 2", ["1", "+", "2"]),
    ("12.5*3", ["12.5", "*", "3"]),
    ("(1+2)*3", ["(", "1", "+", "2", ")", "*", "3"]),
    ("  -5  ", ["-", "5"]),
])
def test_tokenize_ok(expr, expected):
    assert tokenize(expr) == expected


def test_tokenize_bad_char():
    with pytest.raises(ValueError):
        tokenize("1 + a")


def test_tokenize_bad_number():
    with pytest.raises(ValueError):
        tokenize("1.2.3")


@pytest.mark.parametrize("expr,expected", [
    ("1+2", "1 2 +"),
    ("1+2*3", "1 2 3 * +"),
    ("(1+2)*3", "1 2 + 3 *"),
    ("2*(3+4)-5", "2 3 4 + * 5 -"),
    ("-5+3", "5 u- 3 +"),
    ("2*-3", "2 3 u- *"),
    ("-(1+2)", "1 2 + u-"),
])
def test_rpn(expr, expected):
    assert readInput(expr) == expected


@pytest.mark.parametrize("bad", ["(1+2", "1+2)", "1+", "()", "1 2"])
def test_rpn_errors(bad):
    with pytest.raises(ValueError):
        readInput(bad)


@pytest.mark.parametrize("expr,expected", [
    ("1+2", 3.0),
    ("1+2*3", 7.0),
    ("(1+2)*3", 9.0),
    ("10/4", 2.5),
    ("-5+3", -2.0),
    ("2*-3", -6.0),
    ("-(1+2)", -3.0),
    ("((2/(1 + 1)+3)*4/16+1)", 2.0)
])
def test_calculate(expr, expected):
    assert calculate(expr) == expected


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate("1/0")


def test_empty_expression():
    with pytest.raises(ValueError):
        calculate("")