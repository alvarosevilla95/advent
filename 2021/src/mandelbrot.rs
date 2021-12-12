use macroquad::prelude::*;
use num::Complex;
use rayon::prelude::*;

pub async fn run() {
    let mut w = screen_width();
    let mut h = screen_height();
    let mut texture = Texture2D::empty();
    let resolution = 1000_i32;
    let mut zoom = 250_f64;
    let mut off = (-0.5, 0.);
    let mut start;
    let mut needs_update = true;
    loop {
        if is_key_down(KeyCode::E) {
            needs_update = true;
            zoom *= 2.;
        }
        if is_key_down(KeyCode::Q) {
            needs_update = true;
            zoom /= 2.;
        }
        let mut key_rot = |key: KeyCode, v: (f64, f64)| {
            if is_key_down(key) {
                needs_update = true;
                off = (
                    off.0 + v.0 * 250. / zoom as f64,
                    off.1 + v.1 * 250. / zoom as f64,
                );
            }
        };
        key_rot(KeyCode::W, (0., 1.));
        key_rot(KeyCode::A, (1., 0.));
        key_rot(KeyCode::S, (0., -1.));
        key_rot(KeyCode::D, (-1., 0.));
        needs_update |= w != screen_width() || h != screen_height();

        if needs_update {
            w = screen_width();
            h = screen_height();
            start = (
                (-resolution / 2) as f64 / zoom + off.0 as f64,
                (-resolution / 2) as f64 / zoom + off.1 as f64,
            );

            let size = (resolution * resolution * 4) as usize;
            let mut v = vec![0; size];
            v.par_chunks_mut(4).enumerate().for_each(|(i, v)| {
                let x = start.0 + (i as i32 % resolution) as f64 / zoom as f64;
                let y = start.1 + (i as i32 / resolution) as f64 / zoom as f64;
                let p = match mandelbrot_optimized(x, y) {
                    None => 0,
                    Some(d) => (100 - d / 100) as u8,
                };
                for k in v.iter_mut().take(3) {
                    *k = p;
                }
                v[3] = 255;
            });

            texture = Texture2D::from_image(&Image {
                bytes: v,
                width: resolution as u16,
                height: resolution as u16,
            });
        }
        needs_update = false;

        draw_texture_ex(
            texture,
            0.,
            0.,
            WHITE,
            DrawTextureParams {
                dest_size: Some(vec2(w, h)),
                ..Default::default()
            },
        );
        draw_text(format!("{}", get_fps()).as_str(), 10.0, 20.0, 30.0, WHITE);

        next_frame().await
    }
}

pub fn mandelbrot(x: f64, y: f64) -> Option<u32> {
    let start = Complex::new(x, y);
    let mut acc = start;
    for i in 0..255_i32 {
        acc = start + acc.powf(2.);
        if acc.norm() > 4. {
            return Some(i as u32);
        }
    }
    None
}

pub fn mandelbrot_optimized(x: f64, y: f64) -> Option<u32> {
    let x = x as f64;
    let y = y as f64;
    let start_real = x;
    let start_imag = y;
    let mut real = x;
    let mut imag = y;
    let mut real2 = x * x;
    let mut imag2 = y * y;
    for i in 0..1000_i32 {
        imag = (real + real) * imag + start_imag;
        real = real2 - imag2 + start_real;
        real2 = real * real;
        imag2 = imag * imag;
        if real2 + imag2 > 4. {
            return Some(i as u32);
        }
    }
    None
}

extern crate test;

#[cfg(test)]
mod tests {
    use super::mandelbrot;
    use super::mandelbrot_optimized;
    use super::test::black_box;
    use super::test::Bencher;

    #[bench]
    fn bench_mandelbrot(b: &mut Bencher) {
        b.iter(|| {
            (0..100).for_each(|i| {
                black_box(mandelbrot(i as f64, i as f64));
            });
        })
    }

    #[bench]
    fn bench_mandelbrot_optimized(b: &mut Bencher) {
        b.iter(|| {
            black_box((0..100).for_each(|i| {
                black_box(mandelbrot_optimized(i as f64, i as f64));
            }))
        })
    }
}
