# Symmetric Encryption

**Built in:** [Week 6](../weeks/week-06-2026-02-09.md)
**Code:** [security/encryption/symmetric](https://github.com/RGirish/monorepo/tree/main/code/security/encryption/symmetric)

---

## What It Is

An implementation of symmetric encryption — the class of encryption algorithms where the same key is used to both encrypt and decrypt data. This is in contrast to asymmetric (public-key) encryption where different keys are used for each operation.

## Core Concepts

### Shared Key
Both the sender and receiver must possess the same secret key. The security of the system depends entirely on keeping this key secret. Key distribution (how do two parties securely agree on a key?) is the fundamental challenge of symmetric encryption.

### Block Ciphers
A block cipher encrypts a fixed-size block of data (e.g., 128 bits for AES). Longer messages are processed in blocks, and the **mode of operation** determines how blocks are chained or processed.

### Modes of Operation

| Mode | Description | Properties |
|------|-------------|------------|
| **ECB** (Electronic Codebook) | Each block encrypted independently | Simple but insecure — identical plaintext blocks produce identical ciphertext blocks |
| **CBC** (Cipher Block Chaining) | Each block XORed with the previous ciphertext before encrypting | Requires IV; secure but not parallelizable for encryption |
| **CTR** (Counter) | Encrypts a counter value and XORs with plaintext | Parallelizable, no padding needed, widely used |

### Padding
Block ciphers require input to be a multiple of the block size. PKCS#7 padding is the standard: append N bytes each with value N to pad to the next block boundary.

## Why It Matters

Symmetric encryption is the backbone of most data-at-rest and data-in-transit security. TLS uses symmetric encryption for bulk data transfer (after asymmetric key exchange). AES-256-GCM is the modern standard for authenticated encryption.

## Related Builds

- [Two-Phase Commit](two-phase-commit.md) — another systems-level build from the same period
