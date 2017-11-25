from itertools import chain
from collections import defaultdict


class MockError(Exception): pass


class Call:
    def __init__(self, args, kwargs):
        self._key = args, frozenset(kwargs.items())

    def __eq__(self, other):
        return self._key == other._key

    def __hash__(self):
        return hash(self._key)

    def __repr__(self):
        args, kwargs = self._key
        args = [str(v) for v in args]
        kwargs = ["{}={}".format(k, v) for k, v in kwargs]
        return ", ".join(chain(args, kwargs))


class Expectation:
    def __init__(self):
        self._count = 1

    @property
    def met(self):
        return self._count == 0


class Mock:
    def __init__(self):
        self._expectations = dict()
        self._methods = defaultdict(Mock)

    def expect_call(self, *args, **kwargs):
        self._expectations[Call(args, kwargs)] = Expectation()

    def _all_expectations_met(self):
        return (all(e.met for e in self._expectations.values())
                and all(m._all_expectations_met() for m in self._methods.values()))

    def __call__(self, *args, **kwargs):
        call = Call(args, kwargs)
        expectation = self._expectations.get(call, None)
        if expectation is None or not expectation._count:
            raise MockError("unexpected call with arguements: {}, expected: {}".format(call, self._expectations.keys()))
        else:
            expectation._count -= 1

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if not self._all_expectations_met():
            raise MockError()

    def __getattr__(self, name):
        return self._methods[name]
