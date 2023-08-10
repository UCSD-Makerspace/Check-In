import pytest

def func():
    x = 1 + 1
    return x

def test_answer():
    assert func() == 3