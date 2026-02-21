from threading import Lock, Event
from typing import Callable


class PrintAlternativelyUsingLocks:
    def __init__(self, n):
        self.n = n
        self.foolock = Lock()
        self.barlock = Lock()
        self.barlock.acquire()

    def foo(self, printFoo: 'Callable[[], None]') -> None:
        for i in range(self.n):
            self.foolock.acquire()
            # printFoo() outputs "foo". Do not change or remove this line.
            printFoo()
            self.barlock.release()

    def bar(self, printBar: 'Callable[[], None]') -> None:
        for i in range(self.n):
            self.barlock.acquire()
            # printBar() outputs "bar". Do not change or remove this line.
            printBar()
            self.foolock.release()


class PrintAlternativelyUsingEvents:
    def __init__(self, n):
        self.n = n
        self.fooevent = Event()
        self.barevent = Event()
        self.barevent.set()

    def foo(self, printFoo: 'Callable[[], None]') -> None:
        for i in range(self.n):
            self.barevent.wait()
            self.barevent.clear()
            # printFoo() outputs "foo". Do not change or remove this line.
            printFoo()
            self.fooevent.set()

    def bar(self, printBar: 'Callable[[], None]') -> None:
        for i in range(self.n):
            self.fooevent.wait()
            self.fooevent.clear()
            # printBar() outputs "bar". Do not change or remove this line.
            printBar()
            self.barevent.set()
