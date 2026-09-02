import numpy as np

np.random.seed(42)

NUM_VECTORS = 1000
DIMENSIONS = 1536

embeddings = np.random.normal(loc=0.0, scale=0.1, size=(NUM_VECTORS, DIMENSIONS)).astype(np.float32)
embeddings /= np.linalg.norm(embeddings, axis=1, keepdims=True)

vmin = embeddings.min()
vmax = embeddings.max()
scale = (vmax - vmin) / 255

sample = embeddings[0, :5]

print(f"Calibration (computed once, across ALL 1000 x 1536 values): vmin={vmin:.4f}  scale={scale:.6f}\n")

header = f"{'original x':>12} | {'x - vmin':>10} | {'/scale':>10} | {'-128 (pre-round)':>17} | {'round -> q (int8)':>18} | {'q + 128':>8} | {'*scale':>10} | {'+vmin = x_recon':>15} | {'error (x - x_recon)':>20}"
print(header)
print("-" * len(header))

for x in sample:
    step1 = x - vmin
    step2 = step1 / scale
    step3 = step2 - 128
    q = np.round(step3).astype(np.int8)

    d1 = int(q) + 128
    d2 = d1 * scale
    x_recon = d2 + vmin
    error = x - x_recon

    print(f"{x:12.6f} | {step1:10.6f} | {step2:10.4f} | {step3:17.4f} | {q:18d} | {d1:8d} | {d2:10.6f} | {x_recon:15.6f} | {error:20.6f}")
