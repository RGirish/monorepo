from abc import ABC, abstractmethod

import mmh3


class Bloom(ABC):
    @abstractmethod
    def add(self, s: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def contains(self, s: str) -> bool:
        raise NotImplementedError


class Hash(ABC):
    @abstractmethod
    def hash(self, s: str) -> int:
        raise NotImplementedError


class MurmurHash(Hash):
    def hash(self, s: str) -> int:
        return mmh3.hash128(s, 0)


class TerribleBloomFilter(Bloom):
    def __init__(self, hash_fn: Hash):
        self._LENGTH = 100
        self._array = [0] * self._LENGTH
        self._hash_fn = hash_fn

    def add(self, s: str) -> None:
        digest = self._hash_fn.hash(s)
        val = digest % self._LENGTH
        self._array[val] = 1

    def contains(self, s: str) -> bool:
        digest = self._hash_fn.hash(s)
        val = digest % self._LENGTH
        return self._array[val] == 1


if __name__ == '__main__':
    bf = TerribleBloomFilter(MurmurHash())
    for word in [
        "Girish",
        "Bloom",
        "Filter",
        "I believe",
        "Dabba",
    ]:
        bf.add(word)

    for word in [
        "Girish",
        "Bloom",
        "Filter",
        "Hey",
        "Basic Being Basic",
        "I believe",
        "Yo",
        "12345",
        "Dabba",
    ]:
        print(f"{word}: {bf.contains(word)}")
