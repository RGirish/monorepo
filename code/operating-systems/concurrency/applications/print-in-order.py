from threading import Lock, Semaphore, Event
from typing import Callable


class PrintInOrderWithLocks:
    def __init__(self):
        self.l1 = Lock()
        self.l2 = Lock()
        self.l1.acquire()
        self.l2.acquire()

    def first(self, printFirst: 'Callable[[], None]') -> None:
        # printFirst() outputs "first". Do not change or remove this line.
        printFirst()
        self.l1.release()

    def second(self, printSecond: 'Callable[[], None]') -> None:
        self.l1.acquire()
        # printSecond() outputs "second". Do not change or remove this line.
        printSecond()
        self.l2.release()

    def third(self, printThird: 'Callable[[], None]') -> None:
        self.l2.acquire()
        # printThird() outputs "third". Do not change or remove this line.
        printThird()


class PrintInOrderWithSemaphores:
    def __init__(self):
        self.sem1 = Semaphore()
        self.sem2 = Semaphore()
        self.sem1.acquire()
        self.sem2.acquire()

    def first(self, printFirst: 'Callable[[], None]') -> None:
        # printFirst() outputs "first". Do not change or remove this line.
        printFirst()
        self.sem1.release()

    def second(self, printSecond: 'Callable[[], None]') -> None:
        self.sem1.acquire()
        # printSecond() outputs "second". Do not change or remove this line.
        printSecond()
        self.sem2.release()

    def third(self, printThird: 'Callable[[], None]') -> None:
        self.sem2.acquire()
        # printThird() outputs "third". Do not change or remove this line.
        printThird()


class PrintInOrderWithEvents:
    def __init__(self):
        self.e1 = Event()
        self.e2 = Event()

    def first(self, printFirst: 'Callable[[], None]') -> None:
        # printFirst() outputs "first". Do not change or remove this line.
        printFirst()
        self.e1.set()

    def second(self, printSecond: 'Callable[[], None]') -> None:
        self.e1.wait()
        # printSecond() outputs "second". Do not change or remove this line.
        printSecond()
        self.e2.set()

    def third(self, printThird: 'Callable[[], None]') -> None:
        self.e2.wait()
        # printThird() outputs "third". Do not change or remove this line.
        printThird()
