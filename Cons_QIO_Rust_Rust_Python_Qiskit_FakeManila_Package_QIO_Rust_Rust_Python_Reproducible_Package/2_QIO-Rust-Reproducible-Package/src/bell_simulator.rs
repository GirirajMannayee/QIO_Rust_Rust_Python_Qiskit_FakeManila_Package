#[derive(Clone, Copy, Debug)]
struct C { re: f64, im: f64 }

fn add(a:C,b:C)->C { C{re:a.re+b.re, im:a.im+b.im} }
fn scale(a:C,s:f64)->C { C{re:a.re*s, im:a.im*s} }

pub fn phi_plus() -> [C;4] {
    let z=C{re:0.0,im:0.0};
    [scale(C{re:1.0,im:0.0},1.0/2.0_f64.sqrt()), z, z,
     scale(C{re:1.0,im:0.0},1.0/2.0_f64.sqrt())]
}

pub fn psi_plus() -> [C;4] {
    let z=C{re:0.0,im:0.0};
    [z, scale(C{re:1.0,im:0.0},1.0/2.0_f64.sqrt()),
     scale(C{re:1.0,im:0.0},1.0/2.0_f64.sqrt()), z]
}

pub fn demo() {
    println!("Bell simulator: Phi+ = (|00> + |11>)/sqrt(2)");
    println!("Bell simulator: Psi+ = (|01> + |10>)/sqrt(2)");
}
