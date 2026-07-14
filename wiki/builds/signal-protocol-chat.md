# Signal Protocol Chat

**Built in:** [Week 15](../weeks/week-15-2026-04-13.md)
**Code:** `code/security/signal-protocol-chat/` (Android/Kotlin, Jetpack Compose UI)

---

## What It Is

A local, single-device simulation of a 2-person end-to-end encrypted chat using Signal's own `org.signal:libsignal-android` library — the real implementation Signal, WhatsApp, and Messenger's secret conversations run in production, not a reimplementation of the math. Alice and Bob each get their own isolated identity, key material, and session state; the only thing they share is a simulated "wire" carrying opaque ciphertext, which each side decrypts independently using its own keys.

Deliberately out of scope for this build: a real network relay between separate devices, persistent (on-disk) session storage, and Play Store deployment. Those are tracked as a follow-up backlog item — see `wiki/backlog.md`.

---

## Core Concepts

### PQXDH: X3DH Upgraded for Post-Quantum Security

Each user publishes a **pre-key bundle** the other side fetches to start a conversation asynchronously (no live handshake required — the defining problem X3DH solves, versus predecessors like OTR which needed both parties online simultaneously):

| Key | Lifetime | Signed by identity key? | Purpose |
|---|---|---|---|
| Identity key | Long-term | — (this *is* the trust anchor) | Proves who you're talking to |
| Signed pre-key | Medium-term, rotated periodically | Yes | Authenticates the bundle against silent server substitution |
| One-time pre-key | Single-use, deleted after use | No | Adds forward secrecy to one session; not a trust anchor |
| Kyber pre-key | Medium-term, rotated periodically | Yes | Post-quantum shared secret (ML-KEM/Kyber-1024), mixed alongside the classical ECDH result |

The signed and Kyber pre-keys need a signature because they're reused across every sender who starts a session during their rotation window — an unsigned, server-swappable key there would let a compromised server silently man-in-the-middle every new conversation. The one-time pre-key doesn't need one: it's consumed exactly once, so it can't be leveraged for repeatable impersonation, and authentication is already fully handled by the signed pre-key.

**Why Kyber at all:** classical ECDH's security rests on the elliptic curve discrete log problem, which a sufficiently powerful quantum computer (via Shor's algorithm) could break — including retroactively, on ciphertext harvested today. Kyber is a lattice-based **KEM (Key Encapsulation Mechanism)** believed to resist quantum attacks. PQXDH derives the root key from *both* the classical DH result and the Kyber-encapsulated secret, so the session stays protected even if one of the two math problems is later broken.

### The Double Ratchet

Two ratchets running together, both one-way (deletable state, no path backward):

- **DH ratchet** — a fresh ephemeral key pair is generated roughly every round-trip; injects new randomness into the root key that a past compromise couldn't have seen
- **Symmetric-key (KDF) ratchet** — within a turn, `message_key = HMAC(chain_key, 0x01)` and `chain_key' = HMAC(chain_key, 0x02)` are both derived from the *chain key*, not from each other — so leaking one message key doesn't expose the next, because HMAC can't be inverted back to the chain key that produced it

| | Protects | Mechanism |
|---|---|---|
| Forward secrecy | Past messages, from a future key compromise | Symmetric-key ratchet — old keys deleted immediately after use |
| Post-compromise security | Future messages, from a past key compromise | DH ratchet — fresh randomness the attacker never saw gets mixed in every turn |

### Session Asymmetry

Only the initiator runs a live `SessionBuilder.process(bundle)` up front. The responder has no session at all until they decrypt the initiator's first message — a `PreKeySignalMessage`, which carries the sender's identity/base key and which of the recipient's pre-keys were used, embedded right in the ciphertext header. Decryption *is* what builds the responder's side of the session; every message after that is a plain `SignalMessage` with no such header. The build's UI makes this concrete: Bob's send button stays disabled until he's received and decrypted a first message from Alice.

---

## History

Signal Protocol's lineage: **OTR** (2004) had ratcheting for forward secrecy but required both parties online (synchronous). **TextSecure** introduced the **Axolotl Ratchet** (2013) — the asynchronous version, later renamed the Double Ratchet. **WhatsApp** adopted it in 2014–2016, instantly making it the largest E2E-encrypted deployment in history (~1B users). It's since been extended with **PQXDH** for post-quantum resistance, which is what this build actually implements.

---

## See Also

- [Week 15](../weeks/week-15-2026-04-13.md)
- [Cryptography Fundamentals](../concepts/cryptography.md) — how this build's ratcheting/KEM concepts extend the symmetric/asymmetric fundamentals from weeks 6 and 14
- [Asymmetric Encryption](asymmetric-encryption.md) — RSA/OAEP/PSS; the single-exchange counterpart to this build's continuously-rekeying approach
- [Symmetric Encryption](symmetric-encryption.md) — AES; the bulk-cipher half of the hybrid pattern Signal Protocol also relies on internally
