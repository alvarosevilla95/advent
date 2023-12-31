// https://adventofcode.com/2021/day/13

use itertools::Itertools;
use macroquad::prelude::*;

use crate::{utils::*, world2d::World2D};

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

    let mut canvas: World2D<(i32, i32)> = World2D {
        camera: Camera2D {
            zoom: vec2(1. / 40., 1. / 40.),
            target: vec2(20., 0.),
            ..Default::default()
        },
        ..Default::default()
    };
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
        canvas.draw_pixels(&dots, 6).await;
    }
    canvas.draw_pixels(&dots, 6900).await;
}
