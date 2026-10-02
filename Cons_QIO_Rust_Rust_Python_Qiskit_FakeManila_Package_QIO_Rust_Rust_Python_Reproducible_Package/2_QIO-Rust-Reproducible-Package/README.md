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
