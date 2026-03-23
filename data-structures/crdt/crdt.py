from dataclasses import dataclass, field
from typing import Tuple, Optional, List, Union


@dataclass
class Character:
    id: Tuple[str, int]                  # (machine_id, counter) — stable, unique identity
    value: str                           # the actual character, e.g. "a"
    deleted: bool = False                # tombstone — marked deleted but never removed


@dataclass
class InsertOp:
    char_id: Tuple[str, int]
    value: str
    left_id: Optional[Tuple[str, int]]


@dataclass
class DeleteOp:
    char_id: Tuple[str, int]


Op = Union[InsertOp, DeleteOp]


class Network:
    """In-memory broker — documents subscribe and publish ops through it.

    Offline documents have ops queued for them; the queue is flushed when they reconnect.
    """

    def __init__(self):
        self._online: List["Document"] = []
        self._offline_queues: dict = {}   # doc -> list of queued ops

    def subscribe(self, doc: "Document") -> None:
        self._online.append(doc)

    def go_offline(self, doc: "Document") -> None:
        self._online.remove(doc)
        self._offline_queues[id(doc)] = []

    def go_online(self, doc: "Document") -> None:
        # flush any ops that were published while doc was offline
        queued = self._offline_queues.pop(id(doc), [])
        for op in queued:
            doc.apply(op)
        self._online.append(doc)

    def publish(self, sender: "Document", op: Op) -> None:
        for doc in self._online:
            if doc is not sender:
                doc.apply(op)
        # queue op for offline subscribers (excluding sender)
        for doc_id, queue in self._offline_queues.items():
            if doc_id != id(sender):
                queue.append(op)


@dataclass
class Document:
    machine_id: str                      # this machine's unique identity
    network: Optional["Network"] = None  # broker to publish ops to; None = offline
    _chars: List[Character] = field(default_factory=list)
    _counter: int = 0                    # increments each time we insert a character

    def insert(self, value: str, left_id: Optional[Tuple[str, int]]) -> InsertOp:
        """Insert a character locally and broadcast the op to peers."""
        self._counter += 1
        char_id = (self.machine_id, self._counter)
        char = Character(id=char_id, value=value)
        self._apply_insert(char, left_id)
        op = InsertOp(char_id=char_id, value=value, left_id=left_id)
        if self.network:
            self.network.publish(self, op)
        return op

    def delete(self, char_id: Tuple[str, int]) -> DeleteOp:
        """Tombstone a character locally and broadcast the op to peers."""
        for c in self._chars:
            if c.id == char_id:
                c.deleted = True
                break
        op = DeleteOp(char_id=char_id)
        if self.network:
            self.network.publish(self, op)
        return op

    def apply(self, op: Op) -> None:
        """Apply a remote operation."""
        if isinstance(op, InsertOp):
            char = Character(id=op.char_id, value=op.value)
            self._apply_insert(char, op.left_id)
        elif isinstance(op, DeleteOp):
            for c in self._chars:
                if c.id == op.char_id:
                    c.deleted = True
                    break

    def _apply_insert(self, char: Character, left_id: Optional[Tuple[str, int]]) -> None:
        if left_id is None:
            self._chars.insert(0, char)
        else:
            for i, c in enumerate(self._chars):
                if c.id == left_id:
                    self._chars.insert(i + 1, char)
                    break

    def insert_at(self, pos: int, value: str) -> InsertOp:
        """Insert a character at a visible cursor position (0 = before first char)."""
        left_id = self._left_id_at(pos)
        return self.insert(value, left_id)

    def delete_at(self, pos: int) -> Optional[DeleteOp]:
        """Delete the visible character at position pos."""
        visible = [c for c in self._chars if not c.deleted]
        if pos < 0 or pos >= len(visible):
            return None
        return self.delete(visible[pos].id)

    def _left_id_at(self, pos: int) -> Optional[Tuple[str, int]]:
        """Return the id of the visible character just before position pos, or None."""
        visible = [c for c in self._chars if not c.deleted]
        if pos == 0:
            return None
        return visible[pos - 1].id

    def text(self) -> str:
        """Render the document, skipping tombstoned characters."""
        return "".join(c.value for c in self._chars if not c.deleted)
