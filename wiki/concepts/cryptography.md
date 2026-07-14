# Cryptography Fundamentals

Cross-cutting concepts that emerged across Weeks 6, 14, and 15.

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

## Beyond a Single Exchange: Continuous Rekeying

Weeks 6 and 14 both cover a *single* key exchange or encrypted payload. Week 15's Signal Protocol build extends the same asymmetric-encryption foundations (key pairs, signatures, KEMs) into a scheme for an *ongoing conversation*, where the key itself keeps changing:

- **Forward secrecy** — a future key compromise doesn't expose past messages, because old keys are deleted immediately after use and derived via a one-way function (HMAC) that can't be inverted back to its input
- **Post-compromise security** — a past key compromise doesn't expose future messages either, because fresh Diffie-Hellman randomness gets mixed into the shared secret on every round-trip, healing the session even if the attacker never gets caught
- **KEMs (Key Encapsulation Mechanisms)** — Kyber, used for PQXDH, is asymmetric encryption's post-quantum-safe cousin: instead of both sides computing the same DH result, the sender encapsulates a random secret using the recipient's public key, and only the recipient's private key can decapsulate it back out

See [Signal Protocol Chat](../builds/signal-protocol-chat.md) for the full mechanics (X3DH/PQXDH pre-key bundles, the Double Ratchet's two ratchets, why some pre-keys need a signature and others don't).

---

## See Also

- [Symmetric Encryption](../builds/symmetric-encryption.md) — AES block cipher, ECB/CBC/CTR modes (Week 6)
- [Asymmetric Encryption](../builds/asymmetric-encryption.md) — RSA with OAEP + PSS, four attack scenarios (Week 14)
- [Signal Protocol Chat](../builds/signal-protocol-chat.md) — PQXDH + Double Ratchet, forward secrecy and post-compromise security in a real E2E messaging protocol (Week 15)
