mod qbit;
mod measurement;
mod rotation;
mod fitness;
mod collision;
mod sensor_fusion;
mod bell_simulator;
mod ga;
mod pso;
mod scenarios;

fn main() {
    println!("QIO-Rust reproducible simulation package");
    scenarios::run_all();
    bell_simulator::demo();
}
