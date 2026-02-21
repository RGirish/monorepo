from threading import Lock, Condition
from typing import Callable


class ZeroEvenOdd:
    def __init__(self, n):
        self.n = n
        self.i = 1
        lock = Lock()
        self.zero_done = False
        self.c_zero = Condition(lock)
        self.c_odd = Condition(lock)
        self.c_even = Condition(lock)

    def zero(self, printNumber: 'Callable[[int], None]') -> None:
        for _ in range(self.n):
            with self.c_zero:
                printNumber(0)
                self.zero_done = True
                if self.i % 2 == 1:
                    self.c_odd.notify()
                else:
                    self.c_even.notify()
                self.c_zero.wait()

    def odd(self, printNumber: 'Callable[[int], None]') -> None:
        for _ in range((self.n + 1) // 2):
            with self.c_odd:
                if not (self.zero_done and self.i % 2 == 1):
                    self.c_odd.wait()
                printNumber(self.i)
                self.i += 1
                self.zero_done = False
                self.c_zero.notify()

    def even(self, printNumber: 'Callable[[int], None]') -> None:
        for _ in range(self.n // 2):
            with self.c_even:
                if not (self.zero_done and self.i % 2 == 0):
                    self.c_even.wait()
                printNumber(self.i)
                self.i += 1
                self.zero_done = False
                self.c_zero.notify()
