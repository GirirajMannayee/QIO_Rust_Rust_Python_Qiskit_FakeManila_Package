#[derive(Clone, Copy, Debug)]
pub struct QBit { pub alpha: f64, pub beta: f64 }

impl QBit {
    pub fn unbiased() -> Self {
        let a = 1.0_f64 / 2.0_f64.sqrt();
        Self { alpha: a, beta: a }
    }

    pub fn p_one(&self) -> f64 { self.beta * self.beta }

    pub fn normalize(&mut self) {
        let n = (self.alpha*self.alpha + self.beta*self.beta).sqrt();
        if n > 0.0 { self.alpha /= n; self.beta /= n; }
    }
}
