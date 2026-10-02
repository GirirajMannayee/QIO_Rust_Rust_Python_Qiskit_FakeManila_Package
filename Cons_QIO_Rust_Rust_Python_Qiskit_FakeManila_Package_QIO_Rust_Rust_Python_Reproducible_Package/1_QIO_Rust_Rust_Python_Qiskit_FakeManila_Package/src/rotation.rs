use crate::qbit::QBit;

pub fn rotate_toward(q: &mut QBit, target: u8, theta: f64) {
    let c = theta.cos();
    let s = theta.sin();
    let (a,b) = (q.alpha, q.beta);
    if target == 1 {
        q.alpha = c*a - s*b;
        q.beta  = s*a + c*b;
    } else {
        q.alpha = c*a + s*b;
        q.beta  = -s*a + c*b;
    }
    q.normalize();
}
