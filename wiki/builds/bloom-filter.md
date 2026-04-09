# Bloom Filter

**Built in:** [Week 1](../weeks/week-01-2026-01-05.md)
**Code:** [data-structures/bloom-filters](https://github.com/RGirish/monorepo/tree/main/data-structures/bloom-filters)

---

## What It Is

A bloom filter is a probabilistic data structure for answering set membership queries: "Is element X in this set?" It trades perfect accuracy for dramatic space efficiency — a bloom filter uses far less memory than a hash set, at the cost of allowing a small, tunable rate of false positives.

**Key property:** A bloom filter can never produce false negatives. If it says an element is not in the set, it definitely isn't. If it says an element is in the set, it probably is (but might not be).

## How It Works

The data structure is a bit array of size `m`, initially all zeros, and `k` independent hash functions.

**Insert(x):**
1. Hash `x` with each of the `k` hash functions to get `k` bit positions
2. Set all `k` positions to 1 in the bit array

**Query(x):**
1. Hash `x` with each of the `k` hash functions to get `k` bit positions
2. If all `k` positions are 1, return "probably in set"
3. If any position is 0, return "definitely not in set"

**False positive mechanism:** Multiple elements share bit positions (hash collisions). An element might find all its bits set to 1 by a combination of other elements' insertions — producing a false positive.

## Parameters

The false positive rate is tunable via two parameters:
- **m** — size of the bit array (larger → fewer false positives, more memory)
- **k** — number of hash functions (optimal k depends on m and expected set size n)

Optimal `k = (m/n) × ln(2)`. For ~1% false positive rate, you need about 9.6 bits per element.

## Use Cases

- **Web caches** — quickly check if a URL has been cached before doing a full lookup
- **Database query optimization** — check if a key exists before hitting disk
- **Deduplication pipelines** — skip items already seen in a large stream
- **Spell checkers** — fast dictionary membership testing

## Implementation Notes

The implementation uses Python's built-in `hashlib` with different seeds to simulate independent hash functions, and a `bytearray` as the bit array.
