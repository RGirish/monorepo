import os
from typing import ByteString
from cipher import Cipher
from cryptography.hazmat.primitives.ciphers import Cipher as CryptoCipher, algorithms, modes

# AES S-box: derived from multiplicative inverse in GF(2^8) + affine transform
S_BOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
]

# Inverse S-box for decryption
INV_S_BOX = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d,
]

# Round constants for key expansion
RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]


def _xtime(a: int) -> int:
    """Multiply by 2 in GF(2^8) with reduction polynomial x^8 + x^4 + x^3 + x + 1"""
    return ((a << 1) ^ 0x1b) & 0xff if a & 0x80 else (a << 1) & 0xff


def _gf_mul(a: int, b: int) -> int:
    """Multiply two numbers in GF(2^8)"""
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        a = _xtime(a)
        b >>= 1
    return result


class MyAESCipher(Cipher):
    BLOCK_SIZE = 16
    KEY_SIZE = 16  # AES-128
    NUM_ROUNDS = 10

    def _generate_key(self) -> bytes:
        return os.urandom(self.KEY_SIZE)

    def _key_expansion(self, key: bytes) -> list[list[int]]:
        """Expand the key into round keys"""
        words = []
        for i in range(4):
            words.append(list(key[4*i:4*i+4]))

        for i in range(4, 4 * (self.NUM_ROUNDS + 1)):
            temp = words[i - 1][:]
            if i % 4 == 0:
                temp = temp[1:] + temp[:1]
                temp = [S_BOX[b] for b in temp]
                temp[0] ^= RCON[i // 4 - 1]
            words.append([words[i - 4][j] ^ temp[j] for j in range(4)])

        round_keys = []
        for r in range(self.NUM_ROUNDS + 1):
            round_key = []
            for i in range(4):
                round_key.extend(words[r * 4 + i])
            round_keys.append(round_key)
        return round_keys

    def _bytes_to_state(self, b: bytes) -> list[list[int]]:
        """Convert 16 bytes to 4x4 state matrix (column-major)"""
        state = [[0] * 4 for _ in range(4)]
        for i in range(16):
            state[i % 4][i // 4] = b[i]
        return state

    def _state_to_bytes(self, state: list[list[int]]) -> bytes:
        """Convert 4x4 state matrix back to bytes"""
        result = []
        for col in range(4):
            for row in range(4):
                result.append(state[row][col])
        return bytes(result)

    def _add_round_key(self, state: list[list[int]], round_key: list[int]) -> None:
        """XOR state with round key (in-place)"""
        for col in range(4):
            for row in range(4):
                state[row][col] ^= round_key[col * 4 + row]

    def _sub_bytes(self, state: list[list[int]]) -> None:
        """Apply S-box substitution (in-place)"""
        for row in range(4):
            for col in range(4):
                state[row][col] = S_BOX[state[row][col]]

    def _inv_sub_bytes(self, state: list[list[int]]) -> None:
        """Apply inverse S-box substitution (in-place)"""
        for row in range(4):
            for col in range(4):
                state[row][col] = INV_S_BOX[state[row][col]]

    def _shift_rows(self, state: list[list[int]]) -> None:
        """Shift rows left (in-place)"""
        state[1] = state[1][1:] + state[1][:1]
        state[2] = state[2][2:] + state[2][:2]
        state[3] = state[3][3:] + state[3][:3]

    def _inv_shift_rows(self, state: list[list[int]]) -> None:
        """Shift rows right (in-place)"""
        state[1] = state[1][3:] + state[1][:3]
        state[2] = state[2][2:] + state[2][:2]
        state[3] = state[3][1:] + state[3][:1]

    def _mix_columns(self, state: list[list[int]]) -> None:
        """Mix columns using matrix multiplication in GF(2^8) (in-place)"""
        for col in range(4):
            a = [state[row][col] for row in range(4)]
            state[0][col] = _gf_mul(2, a[0]) ^ _gf_mul(3, a[1]) ^ a[2] ^ a[3]
            state[1][col] = a[0] ^ _gf_mul(2, a[1]) ^ _gf_mul(3, a[2]) ^ a[3]
            state[2][col] = a[0] ^ a[1] ^ _gf_mul(2, a[2]) ^ _gf_mul(3, a[3])
            state[3][col] = _gf_mul(3, a[0]) ^ a[1] ^ a[2] ^ _gf_mul(2, a[3])

    def _inv_mix_columns(self, state: list[list[int]]) -> None:
        """Inverse mix columns (in-place)"""
        for col in range(4):
            a = [state[row][col] for row in range(4)]
            state[0][col] = _gf_mul(0x0e, a[0]) ^ _gf_mul(0x0b, a[1]) ^ _gf_mul(0x0d, a[2]) ^ _gf_mul(0x09, a[3])
            state[1][col] = _gf_mul(0x09, a[0]) ^ _gf_mul(0x0e, a[1]) ^ _gf_mul(0x0b, a[2]) ^ _gf_mul(0x0d, a[3])
            state[2][col] = _gf_mul(0x0d, a[0]) ^ _gf_mul(0x09, a[1]) ^ _gf_mul(0x0e, a[2]) ^ _gf_mul(0x0b, a[3])
            state[3][col] = _gf_mul(0x0b, a[0]) ^ _gf_mul(0x0d, a[1]) ^ _gf_mul(0x09, a[2]) ^ _gf_mul(0x0e, a[3])

    def _pad(self, data: bytes) -> bytes:
        """PKCS7 padding"""
        pad_len = self.BLOCK_SIZE - (len(data) % self.BLOCK_SIZE)
        return data + bytes([pad_len] * pad_len)

    def _unpad(self, data: bytes) -> bytes:
        """Remove PKCS7 padding"""
        pad_len = data[-1]
        return data[:-pad_len]

    def _encrypt_block(self, block: bytes, round_keys: list[list[int]]) -> bytes:
        """Encrypt a single 16-byte block"""
        state = self._bytes_to_state(block)

        self._add_round_key(state, round_keys[0])

        for r in range(1, self.NUM_ROUNDS):
            self._sub_bytes(state)
            self._shift_rows(state)
            self._mix_columns(state)
            self._add_round_key(state, round_keys[r])

        self._sub_bytes(state)
        self._shift_rows(state)
        self._add_round_key(state, round_keys[self.NUM_ROUNDS])

        return self._state_to_bytes(state)

    def _decrypt_block(self, block: bytes, round_keys: list[list[int]]) -> bytes:
        """Decrypt a single 16-byte block"""
        state = self._bytes_to_state(block)

        self._add_round_key(state, round_keys[self.NUM_ROUNDS])

        for r in range(self.NUM_ROUNDS - 1, 0, -1):
            self._inv_shift_rows(state)
            self._inv_sub_bytes(state)
            self._add_round_key(state, round_keys[r])
            self._inv_mix_columns(state)

        self._inv_shift_rows(state)
        self._inv_sub_bytes(state)
        self._add_round_key(state, round_keys[0])

        return self._state_to_bytes(state)

    def encrypt(self, m: ByteString) -> ByteString:
        """Encrypt message using ECB mode"""
        padded = self._pad(bytes(m))
        round_keys = self._key_expansion(self._key)
        ciphertext = b''
        for i in range(0, len(padded), self.BLOCK_SIZE):
            block = padded[i:i + self.BLOCK_SIZE]
            ciphertext += self._encrypt_block(block, round_keys)
        return ciphertext

    def decrypt(self, c: ByteString) -> ByteString:
        """Decrypt ciphertext using ECB mode"""
        round_keys = self._key_expansion(self._key)
        plaintext = b''
        for i in range(0, len(c), self.BLOCK_SIZE):
            block = bytes(c[i:i + self.BLOCK_SIZE])
            plaintext += self._decrypt_block(block, round_keys)
        return self._unpad(plaintext)


class AESCipher(Cipher):
    BLOCK_SIZE = 16
    KEY_SIZE = 16  # AES-128

    def _generate_key(self) -> bytes:
        return os.urandom(self.KEY_SIZE)

    def encrypt(self, m: ByteString) -> ByteString:
        nonce = os.urandom(self.BLOCK_SIZE)
        cipher = CryptoCipher(algorithms.AES(self._key), modes.CTR(nonce))
        encryptor = cipher.encryptor()
        return nonce + encryptor.update(bytes(m)) + encryptor.finalize()

    def decrypt(self, c: ByteString) -> ByteString:
        c = bytes(c)
        nonce = c[:self.BLOCK_SIZE]
        ciphertext = c[self.BLOCK_SIZE:]
        cipher = CryptoCipher(algorithms.AES(self._key), modes.CTR(nonce))
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()
