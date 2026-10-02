use rand::Rng;

pub fn sample_binary(n: usize, rng: &mut impl Rng) -> Vec<u8> {
    (0..n).map(|_| if rng.gen::<f64>() < 0.5 {1} else {0}).collect()
}
