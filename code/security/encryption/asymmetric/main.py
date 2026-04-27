"""
Asymmetric encryption demo: Alice sends a signed, encrypted message to Bob.

Concepts demonstrated:
  - RSA key pair generation
  - Encryption with recipient's public key (only recipient can decrypt)
  - Signing with sender's private key (recipient can verify authenticity)
  - Tampering detection via signature verification failure
"""

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


# ── Key generation ────────────────────────────────────────────────────────────
# RSA key pairs: a public key anyone can have, a private key only you hold.
# 2048-bit is the minimum considered secure today; 4096 is more conservative.
# The public exponent 65537 (0x10001) is a standard choice — prime, and fast
# to compute with because it has only two 1-bits in binary.

def generate_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()


# ── Encryption ────────────────────────────────────────────────────────────────
# We use OAEP padding (Optimal Asymmetric Encryption Padding).
# Raw RSA (textbook RSA) is deterministic and malleable — an attacker who sees
# the ciphertext can do math on it to produce a related ciphertext. OAEP adds
# randomness and structure that defeats this.
#
# Note: RSA encryption is only suitable for small payloads (< key size minus
# padding overhead). For real systems you'd encrypt a random AES key with RSA,
# then encrypt the actual message with AES — this is called hybrid encryption.

def encrypt(plaintext: bytes, recipient_public_key) -> bytes:
    return recipient_public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

def decrypt(ciphertext: bytes, recipient_private_key) -> bytes:
    return recipient_private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


# ── Signing & verification ────────────────────────────────────────────────────
# Signing answers "did this really come from Alice?" Encryption alone doesn't —
# anyone could encrypt something with Bob's public key and send it to him.
#
# How it works:
#   1. Alice hashes the plaintext message with SHA-256.
#   2. Alice encrypts that hash with her *private* key → the signature.
#   3. Bob decrypts the signature with Alice's *public* key, getting the hash.
#   4. Bob independently hashes the plaintext and compares. Match = authentic.
#
# PSS (Probabilistic Signature Scheme) is the modern padding for RSA signatures,
# analogous to what OAEP is for encryption.

def sign(message: bytes, sender_private_key) -> bytes:
    return sender_private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )

def verify(message: bytes, signature: bytes, sender_public_key) -> bool:
    try:
        sender_public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except Exception:
        # verify() raises on failure rather than returning False
        return False


# ── In-memory channel ─────────────────────────────────────────────────────────

class Party:
    def __init__(self, name: str):
        self.name = name
        self.private_key, self.public_key = generate_keypair()
        print(f"[{self.name}] Generated RSA-2048 key pair")

    def send(self, plaintext: str, recipient: "Party") -> tuple[bytes, bytes]:
        """Encrypt for recipient and sign with own private key."""
        message_bytes = plaintext.encode()
        ciphertext = encrypt(message_bytes, recipient.public_key)
        signature = sign(message_bytes, self.private_key)
        print(f"[{self.name}] Encrypted + signed message for {recipient.name}")
        return ciphertext, signature

    def receive(self, ciphertext: bytes, signature: bytes, sender: "Party") -> str | None:
        """Decrypt with own private key and verify sender's signature."""
        plaintext = decrypt(ciphertext, self.private_key)
        if verify(plaintext, signature, sender.public_key):
            print(f"[{self.name}] Signature verified ✓  message from {sender.name}: '{plaintext.decode()}'")
            return plaintext.decode()
        else:
            print(f"[{self.name}] Signature INVALID — message rejected")
            return None


# ── Demo ──────────────────────────────────────────────────────────────────────

def main():
    print("=== Key generation ===")
    alice = Party("Alice")
    bob = Party("Bob")

    print("\n=== Normal send ===")
    ciphertext, signature = alice.send("Hello Bob, this is secret!", bob)
    bob.receive(ciphertext, signature, alice)

    print("\n=== Tamper test: Eve modifies the ciphertext ===")
    # Flip a byte in the ciphertext — decryption will fail (OAEP detects corruption)
    tampered = bytearray(ciphertext)
    tampered[42] ^= 0xFF
    try:
        bob.receive(bytes(tampered), signature, alice)
    except Exception as e:
        print(f"[Bob] Decryption failed as expected: {type(e).__name__}")

    print("\n=== Tamper test: Eve replaces the message but reuses Alice's signature ===")
    # Eve encrypts a different message with Bob's public key but can't forge Alice's signature
    evil_ciphertext = encrypt(b"Send Eve all your bitcoin", bob.public_key)
    bob.receive(evil_ciphertext, signature, alice)

    print("\n=== Wrong key test: Charlie tries to decrypt Alice→Bob message ===")
    charlie = Party("Charlie")
    try:
        charlie.receive(ciphertext, signature, alice)
    except Exception as e:
        print(f"[Charlie] Decryption failed as expected: {type(e).__name__}")

    print("\n=== Signature mismatch: message from Charlie, signature from Alice ===")
    ciphertext, _ = charlie.send("Hello Bob, this is secret from Charlie!", bob)
    bob.receive(ciphertext, signature, alice)  # alice's signature over wrong plaintext

if __name__ == "__main__":
    main()
