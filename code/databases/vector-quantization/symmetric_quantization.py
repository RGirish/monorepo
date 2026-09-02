import numpy as np

np.random.seed(42)

NUM_VECTORS = 1000
DIMENSIONS = 1536

embeddings = np.random.normal(loc=0.0, scale=0.1, size=(NUM_VECTORS, DIMENSIONS)).astype(np.float32)
embeddings /= np.linalg.norm(embeddings, axis=1, keepdims=True)


def symmetric_quantize(vectors: np.ndarray) -> tuple[np.ndarray, float]:
    max_abs = np.abs(vectors).max()
    scale = max_abs / 127
    quantized = np.round(vectors / scale).astype(np.int8)
    return quantized, scale


def symmetric_dequantize(quantized: np.ndarray, scale: float) -> np.ndarray:
    return quantized.astype(np.float32) * scale


quantized, scale = symmetric_quantize(embeddings)

print(f"scale: {scale:.6f}")
print(f"Quantized value range: [{quantized.min()}, {quantized.max()}]  (zero maps to: {int(np.round(0 / scale))})")
print(f"Size in memory: {quantized.nbytes / 1024:.1f} KB\n")

# --- The shortcut: compare a raw int8 dot product to the true float dot product ---

query_q = quantized[0].astype(np.int32)     # widen dtype so the accumulation can't overflow int8
all_q = quantized.astype(np.int32)

int_dot_products = all_q @ query_q          # pure integer arithmetic, no floats touched
approx_dot_products = int_dot_products * (scale * scale)   # single correction factor applied once

true_dot_products = embeddings @ embeddings[0]              # the real, full-precision comparison

print("First 5 vectors: true dot product vs. int8-shortcut dot product")
for i in range(5):
    print(f"  true={true_dot_products[i]: .6f}   approx={approx_dot_products[i]: .6f}   "
          f"diff={true_dot_products[i] - approx_dot_products[i]: .6f}   raw_int_dot={int_dot_products[i]}")

max_diff = np.abs(true_dot_products - approx_dot_products).max()
print(f"\nMax dot-product error across all 1000 comparisons: {max_diff:.6f}")

# --- Does search ranking survive using ONLY the integers, never dequantizing? ---

true_ranking = np.argsort(-true_dot_products)
approx_ranking = np.argsort(-approx_dot_products)

top_10_match = len(set(true_ranking[:10]) & set(approx_ranking[:10]))
print(f"Top-10 nearest neighbors overlap (out of 10): {top_10_match}")
