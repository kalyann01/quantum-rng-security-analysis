
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Step 1: Create a quantum circuit
qc = QuantumCircuit(1, 1)

# Step 2: Apply Hadamard gate
qc.h(0)

# Step 3: Measure the qubit
qc.measure(0, 0)

# Step 4: Create quantum simulator
simulator = AerSimulator()

# Step 5: Run 1024 measurements
result = simulator.run(qc, shots=1024).result()

# Step 6: Count zeros and ones
counts = result.get_counts()

zeros = counts.get("0", 0)
ones = counts.get("1", 0)

# Step 7: Display results
print("===== QRNG BASELINE RESULTS =====")
print(qc.draw(output="text"))
print("Total measurements:", zeros + ones)
print("Number of zeros:", zeros)
print("Number of ones:", ones)
print("Percentage of zeros:", round(zeros / 1024 * 100, 2), "%")
print("Percentage of ones:", round(ones / 1024 * 100, 2), "%")
