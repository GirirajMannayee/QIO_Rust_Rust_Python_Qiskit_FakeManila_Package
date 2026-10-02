# QIO-Rust Reproducible Simulation Package

This package implements the manuscript's classical quantum-inspired optimization concepts and supporting Python analysis.

## Important scientific status

The included trial dataset is **SYNTHETIC/SIMULATED DATA**. It is not a record of physical robot measurements and must not be reported as experimental evidence.

## Rust

Requirements: Rust stable toolchain.

Run:

    cargo run --release

The Rust modules include:
- Q-bit-inspired probability representation
- classical measurement
- adaptive rotation
- CNOT-like dependency abstraction
- multi-objective fitness
- collision penalty
- sensor-state fusion
- Bell-state simulator demonstration
- GA/PSO helper components
- S1-S4 scenario execution

## Python

Recommended environment:

    python -m pip install pandas numpy scipy matplotlib openpyxl

From the `python` directory:

    python analyze_trials.py ../data/S1_S4_trial_data.csv
    python statistical_analysis.py ../data/S1_S4_trial_data.csv
    python generate_figures.py ../data/S1_S4_trial_data.csv

## Manuscript mapping

The implementation follows the manuscript concepts: H-like initialization, parameterized rotation, CNOT-like classical coupling, fitness evaluation, measurement, sensor fusion, S1-S4 scenarios, and GA/PSO comparison.

For a final Q1 submission, replace the synthetic CSV with timestamped physical trial data and rerun the analysis.


## Qiskit quantum-circuit validation

Install the current Qiskit components:

    python -m pip install -r requirements-qiskit.txt

Run the ideal simulator:

    python python/qiskit_simulator.py

This validates a two-qubit Bell circuit and a six-qubit grasp-state circuit using Qiskit Aer.

## FakeManilaV2 noisy simulation

Run:

    python python/fake_manila_analysis.py

`FakeManilaV2` is an IBM Quantum backend snapshot used for local testing. The snapshot contains backend characteristics and noise information that can be used to perform a noisy local simulation. This is **not a physical QPU experiment**. The generated counts must therefore be described as fake-backend/noisy-simulation results, not experimental hardware measurements.

The package reports P(00), P(11), and P(other) for the Bell circuit and saves the complete count distribution to `results/fake_manila_bell_counts.csv`.

## Qiskit reproducibility

Run:

    python python/qiskit_environment.py

to record the Python, Qiskit, Qiskit Aer, and Qiskit IBM Runtime versions used for the analysis.
