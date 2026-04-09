from crdt import Character, Document, Network


def test_basic_sync():
    net = Network()
    alice = Document(machine_id="alice", network=net)
    bob = Document(machine_id="bob", network=net)
    net.subscribe(alice)
    net.subscribe(bob)

    # Alice types "a", "c", then inserts "b" between them — Bob gets them automatically
    alice.insert("a", left_id=None)
    alice.insert("c", left_id=("alice", 1))
    alice.insert("b", left_id=("alice", 1))

    assert alice.text() == "abc"
    assert bob.text() == "abc"
    print("test_basic_sync passed")


def test_delete_sync():
    net = Network()
    alice = Document(machine_id="alice", network=net)
    bob = Document(machine_id="bob", network=net)
    net.subscribe(alice)
    net.subscribe(bob)

    alice.insert("a", left_id=None)
    alice.insert("b", left_id=("alice", 1))
    alice.insert("c", left_id=("alice", 2))

    assert alice.text() == "abc"
    assert bob.text() == "abc"

    alice.delete(("alice", 2))

    assert alice.text() == "ac"
    assert bob.text() == "ac"
    print("test_delete_sync passed")


def test_concurrent_insert_and_delete():
    net = Network()
    alice = Document(machine_id="alice", network=net)
    bob = Document(machine_id="bob", network=net)
    net.subscribe(alice)
    net.subscribe(bob)

    # Both start with "ac"
    alice.insert("a", left_id=None)
    alice.insert("c", left_id=("alice", 1))

    assert alice.text() == "ac"
    assert bob.text() == "ac"

    # Go offline
    net.go_offline(alice)
    net.go_offline(bob)

    # Offline: Alice inserts "b" between "a" and "c"
    alice.insert("b", left_id=("alice", 1))
    assert alice.text() == "abc"

    # Offline: Bob deletes "a"
    bob.delete(("alice", 1))
    assert bob.text() == "c"

    # Come back online — queued ops are flushed automatically
    net.go_online(alice)
    net.go_online(bob)

    assert alice.text() == "bc"
    assert bob.text() == "bc"
    print("test_concurrent_insert_and_delete passed")


def test_cursor_api():
    net = Network()
    alice = Document(machine_id="alice", network=net)
    bob = Document(machine_id="bob", network=net)
    net.subscribe(alice)
    net.subscribe(bob)

    # Alice types "ac" then inserts "b" at position 1
    alice.insert_at(0, "a")
    alice.insert_at(1, "c")
    alice.insert_at(1, "b")   # inserts between "a" and "c"

    assert alice.text() == "abc"
    assert bob.text() == "abc"

    # Bob deletes "a" at position 0
    bob.delete_at(0)

    assert alice.text() == "bc"
    assert bob.text() == "bc"
    print("test_cursor_api passed")


if __name__ == "__main__":
    test_basic_sync()
    test_delete_sync()
    test_concurrent_insert_and_delete()
    test_cursor_api()
