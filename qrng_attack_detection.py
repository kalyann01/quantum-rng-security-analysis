
import numpy as np
import matplotlib.pyplot as plt
from math import erfc, sqrt

rng = np.random.default_rng(42)

shots = 1024
trials = 200
attack_rates = [0, 5, 10, 20, 30]
alpha = 0.01

def monobit_pvalue(bits):
    n = len(bits)
    ones = int(np.sum(bits))
    s = 2 * ones - n
    return erfc(abs(s) / sqrt(2 * n))

def generate_bits(attack_rate=0):
    # Simulated ideal quantum measurement
    bits = rng.integers(0, 2, shots)

    # Force selected output bits to 1
    mask = rng.random(shots) < attack_rate / 100
    bits[mask] = 1

    return bits

def detect_attack(bits):
    p_value = monobit_pvalue(bits)
    return p_value < alpha

# Estimate false alarms using normal output
false_alarms = 0

for _ in range(trials):
    bits = generate_bits(0)
    if detect_attack(bits):
        false_alarms += 1

false_alarm_rate = false_alarms / trials * 100

# Evaluate detection at different attack rates
detection_rates = []

for rate in attack_rates:
    detections = 0

    for _ in range(trials):
        bits = generate_bits(rate)

        if detect_attack(bits):
            detections += 1

    detection_rate = detections / trials * 100
    detection_rates.append(detection_rate)

    print(
        f"Attack: {rate}% | "
        f"Detection Rate: {detection_rate:.2f}%"
    )

print(f"\nFalse Alarm Rate: {false_alarm_rate:.2f}%")

# Plot results
plt.plot(
    attack_rates,
    detection_rates,
    marker="o",
    label="Attack Detection Rate"
)

plt.axhline(
    false_alarm_rate,
    color="red",
    linestyle="--",
    label="False Alarm Rate"
)

plt.xlabel("Attack Rate (%)")
plt.ylabel("Detection Rate (%)")
plt.title("QRNG Attack Detection Performance")
plt.ylim(0, 105)
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("qrng_detection_results.png", dpi=300)
plt.show()
