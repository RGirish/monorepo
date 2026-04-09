from threading import Lock, RLock

lock = RLock()
lock.acquire()
lock.acquire()

print("acquired rlock twice")

lock = Lock()
lock.acquire()
lock.acquire()

print("I bet this won't print")
