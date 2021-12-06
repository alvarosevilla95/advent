// https://adventofcode.com/2021/day/5
//
use crate::utils::*;
use array2d::Array2D;
use lazy_static::lazy_static;
use macroquad::prelude::*;
use regex::Regex;

use image::ImageBuffer;
use image::Pixel;
use image::Rgba;
extern crate image;

lazy_static! {
    static ref RE: Regex = Regex::new(r"(\d+),(\d+) -> (\d+),(\d+)").unwrap();
}
pub async fn run() {
    let _input = "0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2";
    let input = get_input(5).await;

    let mut world = Array2D::filled_with(0, 1000, 1000);

    let lines: Vec<((i32, i32), (i32, i32))> = input
        .lines()
        .map(|l| {
            RE.captures(l)
                .map(|c| {
                    (
                        (c[1].parse_i32(), c[2].parse_i32()),
                        (c[3].parse_i32(), c[4].parse_i32()),
                    )
                })
                .unwrap()
        })
        .collect();

    for line in &lines {
        let xr = (line.0 .0, line.1 .0);
        let yr = (line.0 .1, line.1 .1);
        let len = i32::max((xr.0 - xr.1).abs() + 1, (yr.0 - yr.1).abs() + 1);
        for i in 0..len {
            let ni = |r: (i32, i32)| {
                if r.0 == r.1 {
                    0
                } else if r.0 < r.1 {
                    i
                } else {
                    -i
                }
            };

            let xi = ni(xr);
            let yi = ni(yr);

            world[((xr.0 + xi) as usize, (yr.0 as i32 + yi) as usize)] += 1;
        }
    }

    // let dangerous = world.elements_row_major_iter().filter(|p| **p >= 2).count();

    loop {
        let aspect_ratio = world.row_len() as f32 / world.column_len() as f32;
        let screen_aspect_ratio = screen_width() / screen_height();
        let ratio = screen_aspect_ratio - aspect_ratio;
        let x_off = if ratio > 0. {
            screen_width() * (ratio / screen_aspect_ratio)
        } else {
            0.
        };
        let y_off = if ratio < 0. {
            -screen_height() * ratio
        } else {
            0.
        };

        clear_background(Color::new(0., 0., 0.1, 1.0));

        // let wscale = (screen_width() - x_off) / world.row_len() as f32;
        // let hscale = (screen_height() - y_off) / world.column_len() as f32;

        //         for line in &lines {
        //             draw_line(
        //                 line.0 .0 as f32 * wscale + x_off / 2.,
        //                 line.0 .1 as f32 * hscale + y_off / 2.,
        //                 line.1 .0 as f32 * wscale + x_off / 2.,
        //                 line.1 .1 as f32 * hscale + y_off / 2.,
        //                 3.,
        //                 GREEN,
        //             );
        //         }

        let size = 1000;
        let image = ImageBuffer::<Rgba<u8>, Vec<u8>>::from_fn(size, size, |x, y| {
            if world[(x as usize, y as usize)] == 0 {
                Rgba::from_channels(255, 255, 255, 255)
            } else {
                Rgba::from_channels(0, 0, 0, 0)
            }
        });

        let i = Image {
            bytes: image.as_raw().to_vec(),
            width: size as u16,
            height: size as u16,
        };
        let texture = Texture2D::from_image(&i);

        draw_texture_ex(
            texture,
            x_off / 2.,
            y_off / 2.,
            WHITE,
            DrawTextureParams {
                dest_size: Some(vec2(screen_width() - x_off, screen_height() - y_off)),
                ..Default::default()
            },
        );

        draw_text(format!("{}", get_fps()).as_str(), 10.0, 20.0, 30.0, WHITE);
        next_frame().await
    }
}
