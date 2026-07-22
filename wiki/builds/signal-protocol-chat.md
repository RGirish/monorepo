# Signal Protocol Chat

**Built in:** [Week 15](../weeks/week-15-2026-04-13.md)
**Code:** `code/security/signal-protocol-chat/` (Android/Kotlin, Jetpack Compose UI)

---

## What It Is

A real, working end-to-end encrypted chat app between two specific people, over the actual internet, built directly on Signal's own `org.signal:libsignal-android` library — the real implementation Signal, WhatsApp, and Messenger's secret conversations run in production, not a reimplementation of the math. It started as a local, single-device simulation (two in-memory identities exchanging ciphertext through a shared list) and grew, stage by stage, into a genuinely networked app installed on two separate phones.

Deliberately out of scope: pre-key replenishment (the one-time pre-key is never rotated or replaced once consumed) and push notifications (messages only arrive while the app is open, via a live Firestore listener) — both tracked in `wiki/backlog.md`. A formal signed release build / Play Store listing was also skipped in favor of installing directly from Android Studio onto both phones, which is functionally equivalent to sideloading for a two-person app.

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

Only the initiator runs a live `SessionBuilder.process(bundle)` up front. The responder has no session at all until they decrypt the initiator's first message — a `PreKeySignalMessage`, which carries the sender's identity/base key and which of the recipient's pre-keys were used, embedded right in the ciphertext header. Decryption *is* what builds the responder's side of the session; every message after that is a plain `SignalMessage` with no such header. Once the app moved from a shared in-memory list to two independent phones over Firestore, which side ends up as initiator vs. responder became genuinely unpredictable — whichever phone's bundle got published and fetched first wins, and the code handles either outcome the same way.

---

## Real Network Layer (Firebase)

The local two-pane demo (in-memory "Alice"/"Bob" sharing one process) was fully retired and replaced with a real 1:1 chat between two actual devices:

- **Firestore as the relay** — `users/{uid}` holds each person's published pre-key bundle (public keys and signatures only); `messages/{recipientUid}/inbox/{messageId}` holds ciphertext envelopes addressed to them. A live snapshot listener decrypts new envelopes as they arrive and deletes them once delivered, so nothing is ever left around to double-decrypt (which would fail anyway — a used message key is deleted the moment it's used).
- **Persistent on-device storage** — `PersistentSignalProtocolStore` (a full `SignalProtocolStore` implementation backed by files in app-private storage) replaced `InMemorySignalProtocolStore`, so identity and session state survive app restarts instead of resetting every launch. Key material is generated once per fresh store and reloaded on every later launch — regenerating it would silently orphan whatever bundle was already published.
- **Firebase Anonymous Auth for identity** — each install signs in anonymously, getting a stable UID for as long as it stays installed. The app hardcodes the two allowlisted UIDs (kept out of git — see Access Control below) and uses `otherUid()` to resolve "who am I talking to," since there's no dynamic user directory for a fixed two-person app.

### Access Control (not the API key)

A recurring theme of this build: **Firebase project config (`google-services.json`) is not a secret** — it just says which project to talk to, granting no access by itself. The actual gate is **Firestore Security Rules**, deployed server-side, which deny everyone by default and allow read/write only when the request's verified `request.auth.uid` (from a Google-signed JWT, not anything the client can fabricate) is one of the two hardcoded UIDs. Knowing a UID is not equivalent to holding it — the JWT can only be obtained by exchanging a refresh token that's generated once at sign-in and never leaves the device it was issued to; Firebase Anonymous Auth has no "log in as UID X" API. `firestore.rules` (containing both real UIDs) and `local.properties` (which now also injects the two UIDs into `BuildConfig` at build time, keeping them out of `Peers.kt` entirely) are both gitignored, so the public repo contains working code but no way to actually reach this specific deployment.

One concrete hardening applied along the way: `AndroidManifest.xml` originally had `android:allowBackup="true"` (Android's default) — since Firebase Auth's refresh token lives in app-private storage, which Android's Auto Backup would include by default, this was flipped to `false` once the app started holding a real credential worth protecting, closing off cloud-backup as an extraction path.

---

## History

Signal Protocol's lineage: **OTR** (2004) had ratcheting for forward secrecy but required both parties online (synchronous). **TextSecure** introduced the **Axolotl Ratchet** (2013) — the asynchronous version, later renamed the Double Ratchet. **WhatsApp** adopted it in 2014–2016, instantly making it the largest E2E-encrypted deployment in history (~1B users). It's since been extended with **PQXDH** for post-quantum resistance, which is what this build actually implements.

---

## See Also

- [Week 15](../weeks/week-15-2026-04-13.md)
- [Cryptography Fundamentals](../concepts/cryptography.md) — how this build's ratcheting/KEM concepts extend the symmetric/asymmetric fundamentals from weeks 6 and 14
- [Asymmetric Encryption](asymmetric-encryption.md) — RSA/OAEP/PSS; the single-exchange counterpart to this build's continuously-rekeying approach
- [Symmetric Encryption](symmetric-encryption.md) — AES; the bulk-cipher half of the hybrid pattern Signal Protocol also relies on internally
