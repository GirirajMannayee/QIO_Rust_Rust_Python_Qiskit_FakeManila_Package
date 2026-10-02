pub fn velocity_update(v:f64, p_best:f64, g_best:f64, x:f64,
                       w:f64, c1:f64, c2:f64, r1:f64, r2:f64) -> f64 {
    w*v + c1*r1*(p_best-x) + c2*r2*(g_best-x)
}
