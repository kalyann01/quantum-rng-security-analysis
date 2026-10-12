
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError

shots = 1024

print("===== QRNG NOISE SIMULATION =====")

for error_rate in [0.0, 0.05, 0.10, 0.20, 0.30]:

    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    # Asymmetric readout noise
    # 0 may be incorrectly measured as 1
    readout_error = ReadoutError([
        [1 - error_rate, error_rate],
        [0.0, 1.0]
    ])

    noise_model = NoiseModel()
    noise_model.add_all_qubit_readout_error(readout_error)

    simulator = AerSimulator(noise_model=noise_model)

    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts()

    zeros = counts.get("0", 0)
    ones = counts.get("1", 0)

    print(f"\nReadout Error Rate: {error_rate * 100:.0f}%")
    print(f"Zeros: {zeros}")
    print(f"Ones: {ones}")
    print(f"Zero Percentage: {zeros / shots * 100:.2f}%")
    print(f"One Percentage: {ones / shots * 100:.2f}%")
