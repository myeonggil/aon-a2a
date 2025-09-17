from typing import (
    Protocol,
    Sequence,
    Iterable,
    MutableMapping,
    MutableSequence,
    MutableSet,
    NoReturn,
    TypeAlias,
    TypeVar
)
from random import shuffle


TestType = TypeVar("TestType", bound=tuple[int, ...])


class Spam(Protocol):
    def __init__(self, n: int):
        self.n = n

    def __repr__(self):
        return f"Spam({self.n})"

    def __lt__(self, other: 'Spam') -> bool:
        return self.n < other.n


spams = [Spam(n) for n in range(1, 10)]
shuffle(spams)

print(spams)
print(sorted(spams, reverse=False))


def tag(name: str, /, *contains, _class: str | None = None, **attrs: str) -> str:
    print(name, contains)

tag("img", 1, 2)


def test() -> tuple[int, ...]:
    return [1, 2, 3, 4]

print(type(test()))


def double(x):
    return x * 2


class Sample:
    def __init__(self, x):
        self.x = x

    def __mul__(self, x):
        return self.x * x

sample = Sample(100)
print(double(sample))


def f1():
    series = []
    def inner(x):
        series.append(x)
        num = sum(series)
        avg = num / len(series)
        return avg
    return inner

f = f1()
f(10)
res = f(11)
from dis import dis
print(dis(f))
