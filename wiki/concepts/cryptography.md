# Cryptography Fundamentals

Cross-cutting concepts that emerged across Weeks 6 and 14.

---

## The Two Encryption Paradigms

| | Symmetric | Asymmetric |
|---|---|---|
| Keys | One shared secret key | Public + private key pair |
| Speed | Fast (AES has hardware support) | ~1000× slower (big-number math) |
| Key distribution | Hard — how do you share the key securely? | Solved — public key can be shared openly |
| Use case | Bulk data encryption | Key exchange, signatures |
| Built | [Week 6](../weeks/week-06-2026-02-09.md) | [Week 14](../weeks/week-14-2026-04-06.md) |

### The Key Distribution Problem

Symmetric encryption's fundamental challenge: two parties need the same secret key, but how do they agree on it over an untrusted network without an attacker intercepting it? Asymmetric encryption solves this — the recipient publishes their public key openly, the sender uses it to encrypt a shared secret, and only the recipient's private key can unwrap it. The shared secret never travels in plaintext.

---

## Hybrid Encryption

Real systems use both paradigms together:

1. **Asymmetric phase** — use RSA (or ECDH) to securely exchange a random session key; solves key distribution
2. **Symmetric phase** — use AES with that session key for all actual data; solves performance

This is exactly how TLS works. The handshake is asymmetric; everything after is symmetric. RSA is only suitable for small payloads (~190 bytes for a 2048-bit key after OAEP overhead), so it would be impractical for bulk transfer anyway.

---

## What Encryption Alone Doesn't Provide

Encrypting a message with someone's public key guarantees **confidentiality** — only the recipient can read it. But it doesn't guarantee **authenticity** — anyone could encrypt something with the recipient's public key and send it. Digital signatures solve this:

- Sign with sender's **private** key → verify with sender's **public** key
- The signature is over a hash of the plaintext — change the plaintext, the signature fails

Encryption + signing together provides: *only you can read it, and you know who sent it.*

---

## Padding Schemes

Both encryption and signing use probabilistic padding to prevent attacks on raw (textbook) RSA:

| Scheme | Used for | What it adds |
|---|---|---|
| OAEP | Encryption | Random seed; structural checks that detect corruption |
| PSS | Signing | Random salt; prevents deterministic signature forgery |

Raw RSA is deterministic and malleable — the same input always produces the same output, and attackers can manipulate ciphertexts mathematically. Padding schemes break both properties.

---

## See Also

- [Symmetric Encryption](../builds/symmetric-encryption.md) — AES block cipher, ECB/CBC/CTR modes (Week 6)
- [Asymmetric Encryption](../builds/asymmetric-encryption.md) — RSA with OAEP + PSS, four attack scenarios (Week 14)
