from multiprocessing import Process, Value

MAX = 100000
CONCURRENCY = 3


def increment_thread_safe(count):
    for _ in range(MAX):
        with count.get_lock():
            count.value += 1


def increment(count):
    for _ in range(MAX):
        count.value += 1


if __name__ == '__main__':
    count = Value('i', 0)
    for target in [increment, increment_thread_safe]:
        processes = [Process(target=target, args=(count,)) for _ in range(CONCURRENCY)]
        for process in processes:
            process.start()

        for process in processes:
            process.join()

        expected = CONCURRENCY * MAX
        print(f"[{target.__name__}] {expected} == {count.value}: {expected == count.value}")
        count.value = 0
