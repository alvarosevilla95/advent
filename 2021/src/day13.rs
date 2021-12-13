// https://adventofcode.com/2021/day/13

use itertools::Itertools;
use macroquad::prelude::*;

use crate::utils::*;

// The transparent paper is marked with random dots and includes
// instructions on how to fold it up (your puzzle input)
//
// Part 1
// How many dots are visible after completing just the first fold
// instruction on your transparent paper?
//
// Part 2
// Finish folding the transparent paper according to the instructions.
// The manual says the code is always eight capital letters.
// What code do you use to activate the infrared thermal imaging camera system?
pub async fn run() {
    let input = get_input(13).await;
    let _input = "6,10
        0,14
        9,10
        0,3
        10,4
        4,11
        6,0
        6,12
        4,1
        0,13
        10,12
        3,4
        3,0
        8,4
        1,10
        2,14
        8,10
        9,0

        fold along y=7
        fold along x=5";

    let input = input.lines().collect_vec();
    let separator = input
        .iter()
        .enumerate()
        .find(|(_, p)| p.is_empty())
        .map(|(i, _)| i)
        .unwrap();

    let mut dots = input
        .iter()
        .take(separator)
        .map(|l| {
            let (x, y) = l.split(',').collect_tuple().unwrap();
            (x.parse_i32(), y.parse_i32())
        })
        .collect_vec();

    let folds = input.iter().skip(separator + 1).map(|f| {
        let (c, p) = f
            .split(' ')
            .last()
            .unwrap()
            .split('=')
            .collect_tuple::<(&str, &str)>()
            .unwrap();
        (c, p.parse_i32())
    });

    let mut zoom = vec2(1. / 40., 1. / 40.);
    let mut target = vec2(20., 0.);
    for (c, f) in folds {
        for p in &mut dots {
            *p = match (c, &p) {
                ("x", (x, y)) if x > &f => (2 * f - x, *y),
                ("y", (x, y)) if y > &f => (*x, 2 * f - y),
                (_, p) => **p,
            };
        }
        dots.sort_unstable();
        dots.dedup();
        draw_grid(&dots, 6, &mut zoom, &mut target).await;
    }
    draw_grid(&dots, 6000, &mut zoom, &mut target).await;
}

async fn draw_grid(grid: &[(i32, i32)], frames: usize, zoom: &mut Vec2, target: &mut Vec2) {
    for _ in 0..frames {
        clear_background(BLACK);
        if is_key_down(KeyCode::LeftSuper) && is_key_down(KeyCode::Q) {
            return;
        }
        if is_key_down(KeyCode::E) {
            *zoom *= 1.1;
        }
        if is_key_down(KeyCode::Q) {
            *zoom /= 1.1;
        }
        let mut key_rot = |key: KeyCode, v: (f32, f32)| {
            if is_key_down(key) {
                *target = vec2(
                    target[0] + v.0 * 0.05 / zoom[0],
                    target[1] + v.1 * 0.06 / zoom[1],
                );
            }
        };
        key_rot(KeyCode::W, (0., 1.));
        key_rot(KeyCode::A, (-1., 0.));
        key_rot(KeyCode::S, (0., -1.));
        key_rot(KeyCode::D, (1., 0.));

        set_camera(&Camera2D {
            zoom: *zoom,
            target: *target,
            ..Default::default()
        });
        for d in grid {
            draw_rectangle((d.0) as f32, -(d.1) as f32, 1., 1., WHITE);
        }
        next_frame().await;
    }
}
