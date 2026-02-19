import time
from threading import Lock, Thread

lock = Lock()
thread1 = True
thread2 = True


def thread_1():
    global lock, thread1, thread2
    for _ in range(10):
        with lock:
            if not thread2:
                print("1")
        print("sleeping")
        thread1 = False
        time.sleep(0.1)
        thread1 = True


def thread_2():
    global lock, thread1, thread2
    for _ in range(10):
        with lock:
            if not thread1:
                print("2")
        print("sleeping")
        time.sleep(0.1)
        thread2 = False
        time.sleep(0.1)
        thread2 = True


t1 = Thread(target=thread_1)
t2 = Thread(target=thread_2)
t1.start()
t2.start()
t1.join()
t2.join()
