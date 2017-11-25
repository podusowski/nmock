import pytest
from nmock import Mock, MockError


def test_nonexpexted_call():
    m = Mock()
    with pytest.raises(
            MockError, match="unexpected call.*hello") as e:
        m("hello")


def test_nonexpected_call_bacause_args_are_different():
    m = Mock()
    m.expect_call(1, text="hello")

    match = ("unexpected call.*2.*text=hi.*"
             "expected.*1.*text=hello")

    with pytest.raises(MockError, match=match):
        m(2, text="hi")


def test_nonexpected_call_bacause_kwargs_are_different():
    m = Mock()
    m.expect_call(1, text="hello")
    with pytest.raises(MockError):
        m(1, text="hi")


def test_expected_call():
    m = Mock()
    m.expect_call(1, "hello", name="Piotr", place="Wroclaw")
    m(1, "hello", name="Piotr", place="Wroclaw")


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


def test_methods_are_also_mocks():
    with Mock() as m:
        m.foo.expect_call()
        m.foo()


def test_method_mocks_are_checked_in_ctx_manager():
    with pytest.raises(MockError):
        with Mock() as m:
            m.foo.expect_call()
