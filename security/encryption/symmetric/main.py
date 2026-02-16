from cool_but_weak import CaesarCipher
from aes import MyAESCipher, AESCipher

ciphers = [
    CaesarCipher(),
    MyAESCipher(),
    AESCipher(),
]

payload = "journey before destination"
print(f"Original: {payload}")

for cipher in ciphers:
    cipher_bytes = cipher.encrypt(payload.encode())
    print(f"[{cipher.__class__.__name__}] Encrypted: {cipher_bytes.hex()}")
    decrypted_payload = cipher.decrypt(cipher_bytes).decode("UTF-8")
    print(f"[{cipher.__class__.__name__}] Decrypted: {decrypted_payload}")
    assert decrypted_payload == payload, f"{cipher.__class__.__name__} failed round-trip"
    print(f"[{cipher.__class__.__name__}] Round-trip OK")
    print()
