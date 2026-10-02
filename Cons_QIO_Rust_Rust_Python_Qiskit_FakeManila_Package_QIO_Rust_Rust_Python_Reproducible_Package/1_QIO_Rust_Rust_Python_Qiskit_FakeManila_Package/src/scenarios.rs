use rand::thread_rng;
use crate::{qbit::QBit, measurement::measure, rotation::rotate_toward};

pub fn run_all() {
    let names = ["S1","S2","S3","S4"];
    for name in names {
        let mut rng = thread_rng();
        let mut q = vec![QBit::unbiased(); 6];
        for _ in 0..100 {
            let x = measure(&q, &mut rng);
            for (qi, &target) in q.iter_mut().zip(x.iter()) {
                rotate_toward(qi, target, 0.01);
            }
        }
        let final_bits = measure(&q, &mut rng);
        println!("{} final measured grasp state: {:?}", name, final_bits);
    }
}
