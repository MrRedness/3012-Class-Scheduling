"""
This class was created really briefly in order to properly negate the determinism of using
Python sets! Iterating and access is completely random and results in completely variable behavior!
"""

import typing

T = typing.TypeVar("T")

class OrderedSet(typing.MutableSet[T]):
    """A set that preserves insertion order by internally using a dict."""

    def __init__(self, iterable: typing.Iterable[T]):
        self._d = dict.fromkeys(iterable)

    def add(self, x: T) -> None:
        self._d[x] = None

    def discard(self, x: T) -> None:
        self._d.pop(x, None)

    def __contains__(self, x: object) -> bool:
        return self._d.__contains__(x)

    def __len__(self) -> int:
        return self._d.__len__()

    def __iter__(self) -> typing.Iterator[T]:
        return self._d.__iter__()

    def __str__(self):
        return f"{{{', '.join(str(i) for i in self)}}}"

    def __repr__(self):
        return f"<OrderedSet {self}>"