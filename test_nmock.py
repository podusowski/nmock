import pytest
from nmock import Mock, MockError


def test_unexpexted_call():
    m = Mock()
    with pytest.raises(
            MockError, match="unexpected call.*hello") as e:
        m("hello")


def test_expected_different_args():
    m = Mock()
    m.expect_call(1, text="hello")

    match = ("unexpected call.*2.*text=hi.*"
             "expected.*1.*text=hello")

    with pytest.raises(MockError, match=match):
        m(2, text="hi")


def test_expected_different_kwargs():
    m = Mock()
    m.expect_call(1, text="hello")
    with pytest.raises(MockError):
        m(1, text="hi")


def test_expected_call():
    m = Mock()
    m.expect_call(1, "hello", name="Piotr", place="Wroclaw")
    m(1, "hello", name="Piotr", place="Wroclaw")


def test_expected_call_with_mutable_args():
    MUTABLE_ARG1 = {"value": 1}
    MUTABLE_ARG2 = {"value": 2}

    with Mock() as m:
        m.expect_call(MUTABLE_ARG1, key=MUTABLE_ARG2)
        m(MUTABLE_ARG1, key=MUTABLE_ARG2)


def test_same_call_twice():
    m = Mock()
    m.expect_call(1, "hello", name="Piotr", place="Wroclaw")
    m(1, "hello", name="Piotr", place="Wroclaw")
    with pytest.raises(MockError):
        m(1, "hello", name="Piotr", place="Wroclaw")


def test_didnt_make_expected_call():
    with pytest.raises(MockError):
        with Mock() as m:
            m.expect_call()


def test_expected_method_call():
    with Mock() as m:
        m.foo.expect_call()
        m.foo()


def test_missing_expected_method_call():
    with pytest.raises(MockError):
        with Mock() as m:
            m.foo.expect_call()
