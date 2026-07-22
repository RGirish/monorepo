# Signal Protocol Chat (Part 2)

**Built in:** [Week 17](../weeks/week-17-2026-04-27.md) — continues [Part 1](signal-protocol-chat.md) ([Week 15](../weeks/week-15-2026-04-13.md))
**Code:** `code/security/signal-protocol-chat/` (Android/Kotlin, Jetpack Compose UI)

---

## What It Is

Takes Part 1's local, single-device simulation (two in-memory identities exchanging ciphertext through a shared in-process list) and turns it into a real, working end-to-end encrypted chat between two actual phones over the internet. Same underlying `org.signal:libsignal-android` cryptography as Part 1 — this build is entirely about the layer around it: how two independent devices actually find each other, exchange bundles, and deliver messages, and how that's kept secure now that a real backend is involved.

Deliberately out of scope: pre-key replenishment (the one-time pre-key is never rotated or replaced once consumed) and push notifications (messages only arrive while the app is open, via a live Firestore listener) — both tracked in `wiki/backlog.md`. A formal signed release build / Play Store listing was also skipped in favor of installing directly from Android Studio onto both phones, which is functionally equivalent to sideloading for a two-person app.

---

## Real Network Layer (Firebase)

The local two-pane demo (in-memory "Alice"/"Bob" sharing one process) was fully retired and replaced with a real 1:1 chat between two actual devices:

- **Firestore as the relay** — `users/{uid}` holds each person's published pre-key bundle (public keys and signatures only); `messages/{recipientUid}/inbox/{messageId}` holds ciphertext envelopes addressed to them. A live snapshot listener decrypts new envelopes as they arrive and deletes them once delivered, so nothing is ever left around to double-decrypt (which would fail anyway — a used message key is deleted the moment it's used).
- **Persistent on-device storage** — `PersistentSignalProtocolStore` (a full `SignalProtocolStore` implementation backed by files in app-private storage) replaced `InMemorySignalProtocolStore`, so identity and session state survive app restarts instead of resetting every launch. Key material is generated once per fresh store and reloaded on every later launch — regenerating it would silently orphan whatever bundle was already published.
- **Firebase Anonymous Auth for identity** — each install signs in anonymously, getting a stable UID for as long as it stays installed. The app hardcodes the two allowlisted UIDs (kept out of git — see Access Control below) and uses `otherUid()` to resolve "who am I talking to," since there's no dynamic user directory for a fixed two-person app.
- **Session asymmetry, for real this time** — Part 1 already established that only the initiator runs `SessionBuilder.process(bundle)` up front, and the responder's side is built implicitly by decrypting the initiator's first `PreKeySignalMessage`. Once the app moved onto two independent phones over Firestore, which side ends up as initiator vs. responder became genuinely unpredictable — whichever phone's bundle got published and fetched first wins — and the code handles either outcome the same way.

---

## Access Control (Not the API Key)

A recurring theme of this build: **Firebase project config (`google-services.json`) is not a secret** — it just says which project to talk to, granting no access by itself. The actual gate is **Firestore Security Rules**, deployed server-side, which deny everyone by default and allow read/write only when the request's verified `request.auth.uid` (from a Google-signed JWT, not anything the client can fabricate) is one of the two hardcoded UIDs.

Knowing a UID is not equivalent to holding it. A UID shows up in two unrelated places in any given request: as plain data in a Firestore document path (just an address, proves nothing), and separately inside a signed JWT attached to the request as auth metadata (the only thing the server actually trusts). That JWT can only be obtained by exchanging a refresh token generated once at anonymous sign-in and never transmitted anywhere except back to Google — Firebase Anonymous Auth has no "log in as UID X" API, so there's no path from "I know the UID" to "I can authenticate as it" without also holding that refresh token.

`firestore.rules` (containing both real UIDs) and `local.properties` (which injects the two UIDs into `BuildConfig` at build time, keeping them out of `Peers.kt` entirely) are both gitignored, so the public repo contains working code but no way to actually reach this specific deployment.

One concrete hardening applied along the way: `AndroidManifest.xml` originally had `android:allowBackup="true"` (Android's default) — since Firebase Auth's refresh token lives in app-private storage, which Android's Auto Backup would include by default, this was flipped to `false` once the app started holding a real credential worth protecting from cloud-backup extraction.

---

## See Also

- [Signal Protocol Chat](signal-protocol-chat.md) — Part 1 (Week 15); the local crypto simulation this build turns into a real networked app, and where PQXDH/Double Ratchet/forward secrecy/post-compromise security are covered in depth
- [Cryptography Fundamentals](../concepts/cryptography.md) — symmetric/asymmetric fundamentals this build's crypto builds on
