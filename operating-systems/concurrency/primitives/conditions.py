from threading import Condition, Lock

# shared resource
queue = []
queue_lock = Lock()

# multiple conditions on a single shared resource
queue_full = Condition(queue_lock)
queue_empty = Condition(queue_lock)

# you can wait for a condition - when other threads notify on this condition, you'll wake up
queue_full.wait()

# you can notify a thread waiting on a condition
queue_empty.notify()
# you can notify all threads waiting on a condition
queue_empty.notify_all()
