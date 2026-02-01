from abc import ABC, abstractmethod
from random import random
from typing import List


class ICoordinator(ABC):
    @abstractmethod
    def store(self, key) -> None:
        raise NotImplementedError


class IParticipant(ABC):
    @abstractmethod
    def prepare(self, key) -> bool:
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def abort(self) -> None:
        raise NotImplementedError


class TransactionManager(ICoordinator):
    def __init__(self, participants: List[IParticipant]) -> None:
        self._participants = participants

    def store(self, key) -> None:
        # phase 1: prepare
        prepare_results = []
        for participant in self._participants:
            success = participant.prepare(key)
            prepare_results.append(success)

        # phase 2: commit/abort
        if False in prepare_results:
            for participant in self._participants:
                participant.abort()
        else:
            for participant in self._participants:
                participant.commit()


class Node(IParticipant):
    def __init__(self, node_id):
        self._node_id = node_id

    def prepare(self, key) -> bool:
        res = random() < 0.7
        print(f"{self._node_id}: Prepare: {res}")
        return res

    def commit(self) -> None:
        print(f"{self._node_id}: Commit")

    def abort(self) -> None:
        print(f"{self._node_id}: Abort")


if __name__ == '__main__':
    node_1 = Node(1)
    node_2 = Node(2)

    coordinator = TransactionManager([node_1, node_2])
    coordinator.store("a")
