import pytest

###########################################################################
# This is for any test that can be completed on any device before pushing #
###########################################################################

def func():
    x = 1 + 1
    return x

def test_answer():
    assert func() == 3