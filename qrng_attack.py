
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib.pyplot as plt

shots = 10000
attack_rates = [0, 5, 10, 20, 30]

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

simulator = AerSimulator()
counts = simulator.run(qc, shots=shots).result().get_counts()

bits = np.array(
    [int(bit) for bit, count in counts.items()
     for _ in range(count)]
)

rng = np.random.default_rng(42)

normal = np.mean(bits) * 100
noisy = []
attacked = []

for rate in attack_rates:
    p = rate / 100

    # Symmetric random readout errors
    flips = rng.random(len(bits)) < p
    noisy_bits = np.logical_xor(bits, flips)
    noisy.append(np.mean(noisy_bits) * 100)

    # Attack: force selected output bits to 1
    attack_mask = rng.random(len(bits)) < p
    attacked_bits = bits.copy()
    attacked_bits[attack_mask] = 1
    attacked.append(np.mean(attacked_bits) * 100)

print("Rate | Normal | Noise | Attack")
for rate, noise, attack in zip(attack_rates, noisy, attacked):
    print(f"{rate:>3}% | {normal:.2f}% | {noise:.2f}% | {attack:.2f}%")

plt.plot(attack_rates, [normal] * len(attack_rates),
         marker="o", label="Normal QRNG")
plt.plot(attack_rates, noisy,
         marker="s", label="Symmetric noise")
plt.plot(attack_rates, attacked,
         marker="^", label="Forced-one attack")

plt.axhline(50, linestyle="--", color="gray")
plt.xlabel("Noise / Attack Rate (%)")
plt.ylabel("Percentage of Ones (%)")
plt.title("QRNG Security: Normal vs Noise vs Attack")
plt.legend()
plt.grid(True)
plt.savefig("qrng_attack_comparison.png", dpi=300)
plt.show()
