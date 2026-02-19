from threading import Semaphore, BoundedSemaphore

sem = Semaphore(3)
sem.acquire()
sem.acquire()
sem.acquire()
# sem.acquire() blocks
sem.release()
sem.release()
sem.release()
sem.release() # won't throw a ValueError

bsem = BoundedSemaphore(3)
bsem.acquire()
bsem.acquire()
bsem.acquire()
# bsem.acquire() blocks
bsem.release()
bsem.release()
bsem.release()
bsem.release() # throws a ValueError because it's a bounded sem
