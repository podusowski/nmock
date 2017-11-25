from collections import namedtuple


_Expectation = namedtuple("_Expectation", ["args", "kwargs"])


class Mock:
    def __init__(self):
        self._expectations = set()

    def expect_call(self, *args, **kwargs):
        self._expectations.add(_Expectation(args, frozenset(kwargs.items())))

    def __call__(self, *args, **kwargs):
        if _Expectation(args, frozenset(kwargs.items())) not in self._expectations:
            raise RuntimeError()
