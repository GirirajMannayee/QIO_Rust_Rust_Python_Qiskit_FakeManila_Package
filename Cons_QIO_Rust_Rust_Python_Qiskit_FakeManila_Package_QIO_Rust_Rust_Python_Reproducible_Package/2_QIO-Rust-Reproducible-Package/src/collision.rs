pub fn collision_penalty(distance_mm: f64, safety_mm: f64) -> f64 {
    if distance_mm >= safety_mm { 0.0 }
    else { (safety_mm - distance_mm) / safety_mm }
}
