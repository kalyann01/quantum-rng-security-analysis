
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError

error_rates = [0, 5, 10, 20, 30]
zero_percentages = []
one_percentages = []

shots = 10000

for rate in error_rates:
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    error = rate / 100

    readout_error = ReadoutError([
        [1 - error, error],
        [0, 1]
    ])

    noise_model = NoiseModel()
    noise_model.add_all_qubit_readout_error(readout_error)

    simulator = AerSimulator(noise_model=noise_model)
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts()

    zeros = counts.get("0", 0)
    ones = counts.get("1", 0)

    zero_percentages.append(zeros / shots * 100)
    one_percentages.append(ones / shots * 100)

    print(f"Error {rate}%: Zeros={zeros}, Ones={ones}")

plt.figure(figsize=(9, 5))

plt.plot(error_rates, zero_percentages,
         marker="o", label="Zeros (%)")

plt.plot(error_rates, one_percentages,
         marker="s", label="Ones (%)")

plt.axhline(y=50, linestyle="--",
            color="gray", label="Ideal 50%")

plt.xlabel("Asymmetric Readout Error Rate (%)")
plt.ylabel("Output Percentage (%)")
plt.title("QRNG Output Bias Under Readout Noise")
plt.legend()
plt.grid(True)

plt.savefig("qrng_noise_comparison.png", dpi=300)
plt.show()

print("Graph saved as qrng_noise_comparison.png")
