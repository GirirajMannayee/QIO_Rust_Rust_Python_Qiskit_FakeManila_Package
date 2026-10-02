use crate::collision::collision_penalty;

#[derive(Clone, Copy, Debug)]
pub struct Fitness {
    pub total: f64,
    pub stability: f64,
    pub force_error: f64,
    pub collision: f64,
    pub orientation: f64,
    pub trajectory: f64,
    pub computational: f64,
}

pub fn evaluate(stability: f64, force_error: f64, distance_mm: f64,
                orientation: f64, trajectory: f64, computational: f64) -> Fitness {
    let collision = collision_penalty(distance_mm, 20.0);
    let total = 0.25*stability + 0.20*force_error + 0.25*collision
              + 0.10*orientation + 0.10*trajectory + 0.10*computational;
    Fitness { total, stability, force_error, collision, orientation, trajectory, computational }
}
