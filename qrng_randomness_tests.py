
import numpy as np
import matplotlib.pyplot as plt
from math import erfc, sqrt, log2

rng = np.random.default_rng(42)
shots = 10000
rates = [0, 5, 10, 20, 30]

# Simulated ideal QRNG measurement bits
bits = rng.integers(0, 2, shots)

def analyze(data):
    n = len(data)
    ones = int(np.sum(data))
    p = ones / n

    # Shannon entropy per bit
    if p == 0 or p == 1:
        entropy = 0.0
    else:
        entropy = -p*log2(p) - (1-p)*log2(1-p)

    # NIST-style monobit frequency test
    s = 2*ones - n
    p_value = erfc(abs(s) / sqrt(2*n))
    return p, entropy, p_value

print("Rate | Condition | Ones % | Entropy | P-value")

attack_entropy = []
noise_entropy = []

for rate in rates:
    probability = rate / 100

    # Symmetric readout noise
    flips = rng.random(shots) < probability
    noisy = np.logical_xor(bits, flips).astype(int)

    # Forced-one attack
    attacked = bits.copy()
    mask = rng.random(shots) < probability
    attacked[mask] = 1

    for name, data in [("Noise", noisy), ("Attack", attacked)]:
        p, entropy, p_value = analyze(data)

        print(
            f"{rate:>3}% | {name:<9} | "
            f"{p*100:6.2f}% | {entropy:.4f} | "
            f"{p_value:.6f}"
        )

        if name == "Noise":
            noise_entropy.append(entropy)
        else:
            attack_entropy.append(entropy)

plt.plot(rates, noise_entropy, "o-", label="Symmetric noise")
plt.plot(rates, attack_entropy, "s-", label="Forced-one attack")
plt.axhline(1, color="gray", linestyle="--", label="Maximum entropy")

plt.xlabel("Noise / Attack Rate (%)")
plt.ylabel("Shannon Entropy (bits)")
plt.title("QRNG Randomness Under Noise and Attack")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("qrng_entropy_comparison.png", dpi=300)
plt.show()
