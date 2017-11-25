from collections import namedtuple


class Call:
    def __init__(self, args, kwargs):
        self._key = args, frozenset(kwargs.items())

    def __eq__(self, other):
        return self._key == other._key

    def __hash__(self):
        return hash(self._key)


class Expectation:
    def __init__(self):
        self._count = 1


class Mock:
    def __init__(self):
        self._expectations = dict()

    def expect_call(self, *args, **kwargs):
        self._expectations[Call(args, kwargs)] = Expectation()

    def __call__(self, *args, **kwargs):
        call = Call(args, kwargs)
        expectation = self._expectations.get(call, None)
        if expectation is None or not expectation._count:
            raise RuntimeError()
        else:
            expectation._count -= 1
