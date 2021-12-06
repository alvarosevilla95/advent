use image::ImageBuffer;
use image::Pixel;
use image::Rgba;
use macroquad::prelude::*;
use num::Complex;

pub async fn run() {
    let mut image = None;
    let mut w = screen_width();
    let mut h = screen_height();
    let mut texture = Texture2D::empty();
    loop {
        let size = 1000;
        if w != screen_width() || h != screen_height() || image == None {
            w = screen_width();
            h = screen_height();
            image = Some(ImageBuffer::<Rgba<u8>, Vec<u8>>::from_fn(
                size,
                size,
                |x, y| {
                    let scale = |v| ((v as i32 - size as i32 / 2) as f32 / 1000080.0) * 4.0;
                    mandelbrot_optimized(scale(x) - 1., scale(y) + 0.3).map_or_else(
                        || Rgba::from_channels(255, 255, 255, 255),
                        |d| {
                            Rgba::from_channels(
                                (d / 100) as u8,
                                (d / 100) as u8,
                                (d / 100) as u8,
                                255,
                            )
                        },
                    )
                    // return Rgba::from_channels(255, 255, 255, 255);
                },
            ));
            let i = Image {
                bytes: image.as_ref().unwrap().as_raw().to_vec(),
                width: size as u16,
                height: size as u16,
            };
            texture = Texture2D::from_image(&i);
        }

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

pub fn mandelbrot(x: f32, y: f32) -> Option<u32> {
    let start = Complex::new(x, y);
    let mut acc = start;
    for i in 0..500 as i32 {
        acc = start + acc.powf(2.);
        if acc.norm() > 4. {
            return Some(i as u32);
        }
    }
    None
}

pub fn mandelbrot_optimized(x: f32, y: f32) -> Option<u32> {
    let x = x as f64;
    let y = y as f64;
    let start_real = x;
    let start_imag = y;
    let mut real = x;
    let mut imag = y;
    let mut real2 = x * x;
    let mut imag2 = y * y;
    for i in 0..100 as i32 {
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
                black_box(mandelbrot(i as f32, i as f32));
            });
        })
    }

    #[bench]
    fn bench_mandelbrot_optimized(b: &mut Bencher) {
        b.iter(|| {
            black_box((0..100).for_each(|i| {
                black_box(mandelbrot_optimized(i as f32, i as f32));
            }))
        })
    }
}
