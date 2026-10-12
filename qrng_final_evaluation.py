
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Phase 7: Final QRNG Security Evaluation
# Uses simulated attacks, not physical quantum hardware.

rng = np.random.default_rng(42)
simulator = AerSimulator()
SHOTS = 1024
TRIALS = 100
ATTACK_RATES = [0, 5, 10, 20, 30]

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

def generate_qrng():
    result = simulator.run(qc, shots=SHOTS).result()
    counts = result.get_counts()
    zeros = counts.get("0", 0)
    ones = counts.get("1", 0)
    return zeros, ones

def simulate_attack(zeros, ones, rate):
    # Approximation: attacker forces selected zeros to ones.
    changed = rng.binomial(zeros, rate / 100)
    return zeros - changed, ones + changed

def bias_score(zeros, ones):
    return abs(ones / (zeros + ones) - 0.5)

# Calibrate threshold using independent normal samples.
calibration = []
for _ in range(1000):
    z, o = generate_qrng()
    calibration.append(bias_score(z, o))

threshold = np.quantile(calibration, 0.99)
print(f"Calibrated threshold: {threshold:.4f}")

# Evaluate normal and attacked samples.
results = []
for rate in ATTACK_RATES:
    detections = 0
    for _ in range(TRIALS):
        z, o = generate_qrng()
        if rate > 0:
            z, o = simulate_attack(z, o, rate)
        if bias_score(z, o) > threshold:
            detections += 1

    results.append(detections / TRIALS)
    print(f"Attack {rate}%: Flagged {results[-1]*100:.1f}%")

# Plot detection and false-alarm rates.
plt.figure(figsize=(9, 5))
plt.plot(ATTACK_RATES, np.array(results)*100,
         marker="o", label="Flagged samples")
plt.xlabel("Forced-one attack rate (%)")
plt.ylabel("Samples flagged (%)")
plt.title("QRNG Security Evaluation")
plt.ylim(0, 105)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("qrng_final_evaluation.png", dpi=300)
plt.show()

# Binary classification summary for pooled attack cases.
tp = round(sum(results[1:]) * TRIALS)
fn = TRIALS * (len(ATTACK_RATES)-1) - tp
fp = round(results[0] * TRIALS)
tn = TRIALS - fp

precision = tp / (tp + fp) if tp + fp else 0
recall = tp / (tp + fn) if tp + fn else 0
f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0

print("\nFINAL SECURITY METRICS")
print(f"False alarm rate: {fp/TRIALS*100:.2f}%")
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1-score: {f1:.3f}")
print("Graph saved: qrng_final_evaluation.png")
