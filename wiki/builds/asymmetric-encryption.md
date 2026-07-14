# Asymmetric Encryption

**Built in:** [Week 14](../weeks/week-14-2026-04-06.md)
**Code:** `code/security/encryption/asymmetric/main.py`

---

## What It Is

An in-memory simulation of two-party secure communication using RSA asymmetric encryption and digital signatures. Alice encrypts a message so only Bob can read it, and signs it so Bob can verify it came from her. Four tamper/attack scenarios demonstrate what each primitive protects against.

---

## Core Concepts

### The Two Asymmetries

| Operation | Encrypted/signed with | Decrypted/verified with | Protects |
|---|---|---|---|
| Encryption | Recipient's **public** key | Recipient's **private** key | Confidentiality |
| Signing | Sender's **private** key | Sender's **public** key | Authenticity |

They solve different problems. Encryption without signing: you don't know who sent it. Signing without encryption: anyone can read it. You need both.

### OAEP Padding (encryption)

Raw RSA is deterministic and malleable — the same plaintext always produces the same ciphertext, and an attacker can do math on ciphertexts to produce related ciphertexts. OAEP fixes this by transforming the message through a randomised two-block structure before RSA:

```
Block A = seed XOR MGF(padded_message)
Block B = padded_message XOR MGF(seed)
```

The seed is random and fresh each encryption — making the same message produce different ciphertexts every time. The seed is self-recovering: each block is the key to unscrambling the other, so the receiver doesn't need the seed separately. On decryption, OAEP checks structural invariants (label hash, zero-padding, separator byte) — any corruption causes decryption to throw rather than silently return garbage.

**Probability of undetected corruption:** ~1/2²⁵⁶ for the hash check alone. Effectively impossible.

**Can an attacker carefully flip bits to bypass OAEP?** No — they'd need the private key to decrypt first, get the seed, understand the structure, re-scramble, then re-encrypt. The seed is opaque without decryption.

### MGF (Mask Generation Function)

The scrambler used inside OAEP. Takes an input, produces a pseudorandom-looking output of a requested size by repeatedly hashing `input + counter` and concatenating results. Deterministic (same input → same output), but looks like noise. Security doesn't come from MGF being secret — it comes from the RSA layer hiding the inputs to MGF.

### PSS Padding (signing)

The signing equivalent of OAEP. Probabilistic Signature Scheme adds randomness (salt) to the signing process so the same message signed twice produces different signatures. Defeats certain forgery attacks possible with deterministic signing.

### RSA Size Limits

RSA can only encrypt small payloads — a 2048-bit key can encrypt at most ~190 bytes after OAEP overhead. For larger messages, real systems use **hybrid encryption**: encrypt a random AES session key with RSA, then encrypt the actual payload with AES. This is exactly what TLS does during the handshake.

---

## Attack Scenarios Demonstrated

| Scenario | What happens | Why |
|---|---|---|
| Eve flips a byte in ciphertext | Decryption throws `ValueError` | OAEP structural checks fail |
| Eve swaps message, reuses Alice's signature | Signature verification fails | Signature is over the original plaintext hash |
| Charlie tries to decrypt Alice→Bob message | Decryption throws `ValueError` | Wrong private key produces garbage; OAEP detects |
| Bob receives Charlie's message with Alice's old signature | Signature INVALID | Signature doesn't match the decrypted plaintext |

---

## Connection to TLS / SSL

TLS uses both primitives from this build:
1. **Asymmetric encryption** (RSA or ECDH) to securely exchange a session key between strangers — solving the key distribution problem
2. **Symmetric encryption** (AES) for all bulk data transfer, because RSA is ~1000× slower than AES

The asymmetric phase is the handshake; the symmetric phase is everything after. See [Symmetric Encryption](symmetric-encryption.md) for the Week 6 build on the other half.

---

## See Also

- [Week 14](../weeks/week-14-2026-04-06.md)
- [Symmetric Encryption](symmetric-encryption.md) — Week 6 build; the counterpart; AES block cipher with ECB/CBC/CTR modes
- [Cryptography Fundamentals](../concepts/cryptography.md) — how symmetric and asymmetric encryption compose into real systems
- [Signal Protocol Chat](signal-protocol-chat.md) — Week 15 build; extends these same primitives (key pairs, signatures) into a continuously-rekeying scheme for ongoing conversations
