from typing import ByteString
from cipher import Cipher


class CaesarCipher(Cipher):
    def _generate_key(self):
        return 5

    def encrypt(self, m: ByteString) -> ByteString:
        return bytearray([(b + self._key) % 256 for b in m])

    def decrypt(self, c: ByteString) -> ByteString:
        return bytearray([(b - self._key) % 256 for b in c])
