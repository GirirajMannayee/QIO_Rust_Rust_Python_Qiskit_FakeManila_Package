#[derive(Clone, Debug)]
pub struct SensorState {
    pub object_xyz: [f64;3],
    pub proximity_mm: f64,
    pub tactile_force_n: f64,
    pub imu_motion: f64,
    pub measured_force_n: f64,
}

pub fn fuse(camera_xyz: [f64;3], proximity_mm: f64, tactile_force_n: f64,
            imu_motion: f64, measured_force_n: f64) -> SensorState {
    SensorState { object_xyz: camera_xyz, proximity_mm, tactile_force_n,
                  imu_motion, measured_force_n }
}
