from threading import Thread


def target():
    for i in range(100):
        print(f"{i}")


# when main program ends, the daemon thread ends with it whether it's finished executing or not
# thread = Thread(target=target, daemon=True)
# when main program ends, it waits for non-daemon thread to end
thread = Thread(target=target, daemon=False)
thread.start()
