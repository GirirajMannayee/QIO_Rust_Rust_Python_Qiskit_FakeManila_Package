"""Print Qiskit package versions for reproducibility."""
import sys
import qiskit
import qiskit_aer
import qiskit_ibm_runtime

print("Python:", sys.version)
print("Qiskit:", qiskit.__version__)
print("Qiskit Aer:", qiskit_aer.__version__)
print("Qiskit IBM Runtime:", qiskit_ibm_runtime.__version__)
