"""
Fake Manila V2 analysis.

FakeManilaV2 is an IBM QPU snapshot used for local noisy simulation.
It is NOT a real hardware experiment and must not be reported as
physical-device measurements.
"""
from pathlib import Path
import csv

from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
from qiskit_aer import AerSimulator

SHOTS = 4096

def bell():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    return qc

def run_fake_manila():
    backend = FakeManilaV2()

    qc = bell()
    pm = generate_preset_pass_manager(
        backend=backend,
        optimization_level=1
    )
    isa_qc = pm.run(qc)

    # AerSimulator.from_backend applies the fake backend's
    # backend-derived noise model locally.
    noisy_sim = AerSimulator.from_backend(backend)

    result = noisy_sim.run(
        isa_qc,
        shots=SHOTS,
        seed_simulator=42
    ).result()

    counts = result.get_counts()

    print("FakeManilaV2 noisy Bell-state counts:")
    print(counts)

    total = sum(counts.values())
    p00 = counts.get("00", 0) / total
    p11 = counts.get("11", 0) / total
    p_other = 1.0 - p00 - p11

    print(f"P(00)={p00:.4f}")
    print(f"P(11)={p11:.4f}")
    print(f"P(other)={p_other:.4f}")

    out = Path("../results/fake_manila_bell_counts.csv")
    out.parent.mkdir(exist_ok=True)
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["state", "counts", "probability"])
        for state, count in sorted(counts.items()):
            w.writerow([state, count, count/total])

    return counts

if __name__ == "__main__":
    run_fake_manila()
