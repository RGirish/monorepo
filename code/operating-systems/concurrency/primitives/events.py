import time
from threading import Event, Thread

event = Event()


def wait_fn():
    event.wait()


# it doesn't matter if event is set before the wait happens
event.set()

thread = Thread(target=wait_fn)
thread.start()
print("Thread started, waiting")
time.sleep(1)
