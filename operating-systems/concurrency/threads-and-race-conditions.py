from threading import Lock, Thread

count = 0
lock = Lock()
MAX = 100000
CONCURRENCY = 3


def increment_thread_safe():
    global count
    for _ in range(MAX):
        with lock:
            count += 1


def increment():
    """
    Technically appears as if it's thread-safe even without the use of a lock - but it is not. Since += is not an
    atomic operation, and it involves the read-operate-write steps in its bytecode, the GIL could technically context
    switch in the middle of this 3-step bytecode instruction, causing race conditions. We may not see it manifest that
    frequently though.
    """
    global count
    for _ in range(MAX):
        count += 1


threads = [Thread(target=increment) for _ in range(CONCURRENCY)]
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

expected = CONCURRENCY * MAX
print(f"{expected} == {count}: {expected == count}")
