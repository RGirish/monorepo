import time
from threading import Barrier, Thread

barrier = Barrier(3)


def target(thread_id):
    global barrier
    print(f"Thread {thread_id} waiting at barrier")
    barrier.wait()
    time.sleep(1)
    print(f"Thread {thread_id} exiting")


threads = []
for i in range(1, 4):
    thread = Thread(target=target, args=(i,))
    threads.append(thread)
    thread.start()
    time.sleep(1)

for thread in threads:
    thread.join()
