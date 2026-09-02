import numpy as np

np.random.seed(42)

NUM_VECTORS = 1000
DIMENSIONS = 1536

embeddings = np.random.normal(loc=0.0, scale=0.1, size=(NUM_VECTORS, DIMENSIONS)).astype(np.float32)
embeddings /= np.linalg.norm(embeddings, axis=1, keepdims=True)

print(f"Shape: {embeddings.shape}, dtype: {embeddings.dtype}")
print(f"Value range: [{embeddings.min():.4f}, {embeddings.max():.4f}]")
print(f"Size in memory: {embeddings.nbytes / 1024:.1f} KB")


def quantize(vectors: np.ndarray) -> tuple[np.ndarray, float, float]:
    vmin = vectors.min()
    vmax = vectors.max()

    scale = (vmax - vmin) / 255
    quantized = np.round((vectors - vmin) / scale - 128).astype(np.int8)

    return quantized, vmin, scale


quantized, vmin, scale = quantize(embeddings)

print(f"\nQuantized dtype: {quantized.dtype}")
print(f"Quantized value range: [{quantized.min()}, {quantized.max()}]")
print(f"Size in memory: {quantized.nbytes / 1024:.1f} KB")
print(f"Calibration params -> vmin: {vmin:.4f}, scale: {scale:.6f}")


def dequantize(quantized: np.ndarray, vmin: float, scale: float) -> np.ndarray:
    return ((quantized.astype(np.float32) + 128) * scale + vmin)


reconstructed = dequantize(quantized, vmin, scale)

max_abs_error = np.abs(embeddings - reconstructed).max()
mean_abs_error = np.abs(embeddings - reconstructed).mean()
print(f"\nMax absolute error per element: {max_abs_error:.6f}")
print(f"Mean absolute error per element: {mean_abs_error:.6f}")


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a_norm = a / np.linalg.norm(a, axis=1, keepdims=True)
    b_norm = b / np.linalg.norm(b, axis=1, keepdims=True)
    return np.sum(a_norm * b_norm, axis=1)


query = embeddings[0:1]
query_reconstructed = reconstructed[0:1]

true_similarities = cosine_similarity(np.repeat(query, NUM_VECTORS, axis=0), embeddings)
approx_similarities = cosine_similarity(np.repeat(query_reconstructed, NUM_VECTORS, axis=0), reconstructed)

true_ranking = np.argsort(-true_similarities)
approx_ranking = np.argsort(-approx_similarities)

top_10_match = len(set(true_ranking[:10]) & set(approx_ranking[:10]))
print(f"\nTop-10 nearest neighbors overlap (out of 10): {top_10_match}")
print(f"Max similarity score drift: {np.abs(true_similarities - approx_similarities).max():.6f}")
