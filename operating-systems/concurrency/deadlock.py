"""
Simulates deadlocks - (if we're lucky - sometimes, the conditions to warrant a deadlock may not be met if the bytecode
instructions just so happen to execute in such an order) - by including the following conditions:
1. Mutual exclusion
2. Hold & wait
3. Circular wait
4. No preemption
"""
from threading import Lock, Thread

lock1 = Lock()
lock2 = Lock()
val1 = ""
val2 = ""


def thread_1():
    global val1, val2
    print("Thread 1 wants lock 1")
    with lock1:
        print("Thread 1 acquired lock 1")
        val1 = "1"
        print("Thread 1 wants lock 2")
        with lock2:
            print("Thread 1 acquired lock 2")
            val2 = "1"


def thread_2():
    global val1, val2
    print("Thread 2 wants lock 2")
    with lock2:
        print("Thread 2 acquired lock 2")
        val2 = "2"
        print("Thread 2 wants lock 1")
        with lock1:
            print("Thread 2 acquired lock 1")
            val1 = "2"


t1 = Thread(target=thread_1)
t2 = Thread(target=thread_2)
t1.start()
t2.start()
t1.join()
t2.join()
