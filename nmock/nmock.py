from itertools import chain
from collections import defaultdict


class MockError(Exception): pass


class Call:
    def __init__(self, args, kwargs):
        self._args = args
        self._kwargs = kwargs

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        args = [str(v) for v in self._args]
        kwargs = ["{}={}".format(k, v) for k, v in self._kwargs.items()]
        return ", ".join(chain(args, kwargs))


class Expectation:
    def __init__(self, call):
        self._count = 1
        self.call = call

    @property
    def met(self):
        return self._count == 0

    def __repr__(self):
        return repr(self.call)


class Mock:
    def __init__(self):
        self._expectations = list()
        self._methods = defaultdict(Mock)

    def expect_call(self, *args, **kwargs):
        self._expectations.append(Expectation(Call(args, kwargs)))

    def _all_expectations_met(self):
        return (all(e.met for e in self._expectations)
                and all(m._all_expectations_met() for m in self._methods.values()))

    def _find_expectation(self, call):
        for e in self._expectations:
            if e.call == call:
                return e

    def __call__(self, *args, **kwargs):
        call = Call(args, kwargs)
        expectation = self._find_expectation(call)
        if expectation is None or not expectation._count:
            raise MockError("unexpected call with arguements: {}, expected: {}".format(call, self._expectations))
        else:
            expectation._count -= 1

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if not self._all_expectations_met():
            raise MockError("mock was expected to be called with: {}".format(self._expectations))

    def __getattr__(self, name):
        return self._methods[name]
