import pytest
from nmock import Mock


def test_nonexpexted_call():
    m = Mock()
    with pytest.raises(Exception):
        m("hello")


def test_nonexpected_call_bacause_args_are_different():
    m = Mock()
    m.expect_call(1, "hello")
    with pytest.raises(Exception):
        m(2, "hello")


def test_nonexpected_call_bacause_kwargs_are_different():
    m = Mock()
    m.expect_call(1, text="hello")
    with pytest.raises(Exception):
        m(1, text="hi")


def test_expected_call():
    m = Mock()
    m.expect_call(1, "hello", name="Piotr", place="Wroclaw")
    m(1, "hello", name="Piotr", place="Wroclaw")


def test_same_call_twice():
    m = Mock()
    m.expect_call(1, "hello", name="Piotr", place="Wroclaw")
    m(1, "hello", name="Piotr", place="Wroclaw")
    with pytest.raises(Exception):
        m(1, "hello", name="Piotr", place="Wroclaw")
