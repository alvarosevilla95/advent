// https://adventofcode.com/2021/day/13

use std::{thread, time::Duration};

use array2d::Array2D;
use itertools::Itertools;
use macroquad::prelude::*;

use crate::utils::*;

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
    let fold_count = input
        .iter()
        .enumerate()
        .find(|(_, p)| p.is_empty())
        .map(|(i, _)| i)
        .unwrap();

    let dots = &input[0..fold_count];
    let mut dots = dots
        .iter()
        .map(|l| l.split(',').collect_vec())
        .map(|c| (c[0].parse_i32(), c[1].parse_i32()))
        .collect_vec();

    let folds = &input[fold_count + 1..input.len()];
    let folds = folds
        .iter()
        .map(|f| f.split(' ').last().unwrap())
        .map(|f| f.split('=').collect_tuple::<(&str, &str)>().unwrap())
        .map(|p| (p.0, p.1.parse_i32()))
        .collect_vec();

    let mut zoom = vec2(1. / 800., 1. / 800.);
    let mut target = vec2(350., 0.);
    for fold in folds {
        match fold.0 {
            "x" => fold_grid_horizontal(&mut dots, fold.1),
            "y" => fold_grid_vertical(&mut dots, fold.1),
            _ => (),
        }

        draw_grid(&dots, 30, &mut zoom, &mut target).await;
    }
    draw_grid(&dots, 18000000, &mut zoom, &mut target).await;
}

fn fold_grid_horizontal(grid: &mut [(i32, i32)], pos: i32) {
    for p in grid {
        if p.0 > pos {
            p.0 = 2 * pos - p.0
        }
    }
}

fn fold_grid_vertical(grid: &mut [(i32, i32)], pos: i32) {
    for p in grid {
        if p.1 > pos {
            p.1 = 2 * pos - p.1
        }
    }
}

async fn draw_grid(grid: &[(i32, i32)], frames: usize, zoom: &mut Vec2, target: &mut Vec2) {
    for _ in 0..frames {
        clear_background(BLACK);
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
            draw_rectangle(20. * (d.0) as f32, 20. * -(d.1) as f32, 20., 20., WHITE);
        }
        next_frame().await;
    }
}
