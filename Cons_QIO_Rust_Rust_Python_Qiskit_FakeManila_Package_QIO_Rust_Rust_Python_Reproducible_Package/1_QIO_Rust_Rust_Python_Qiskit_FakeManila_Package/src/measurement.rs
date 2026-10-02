use rand::Rng;
use crate::qbit::QBit;

pub fn measure(bits: &[QBit], rng: &mut impl Rng) -> Vec<u8> {
    bits.iter().map(|q| if rng.gen::<f64>() < q.p_one() {1} else {0}).collect()
}
