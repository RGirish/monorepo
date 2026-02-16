import abc
from abc import abstractmethod
from typing import ByteString


class Cipher(abc.ABC):
    def __init__(self):
        self._key = self._generate_key()

    @abstractmethod
    def encrypt(self, m: ByteString) -> ByteString:
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, c: ByteString) -> ByteString:
        raise NotImplementedError

    @abstractmethod
    def _generate_key(self):
        raise NotImplementedError
