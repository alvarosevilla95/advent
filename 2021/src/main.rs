#![feature(nll)]
#![feature(test)]
#![allow(dead_code)]

use macroquad::prelude::*;

extern crate image;

pub mod day01;
pub mod day02;
pub mod day03;
pub mod day04;
pub mod day05;
pub mod day06;
pub mod day07;
pub mod day08;
pub mod day09;
pub mod day10;
pub mod day11;
pub mod day12;
pub mod day13;
pub mod day14;
pub mod day15;
pub mod day16;
// pub mod day17;
// pub mod day18;
// pub mod day19;
// pub mod day20;
// pub mod day21;
// pub mod day22;
// pub mod day23;
// pub mod day24;
// pub mod day25;
pub mod utils;

pub mod evolution;
pub mod graphics;
pub mod life;
pub mod mandelbrot;
pub mod world2d;

fn conf() -> Conf {
    Conf {
        window_title: String::from("Macroquad"),
        window_width: 800,
        window_height: 600,
        high_dpi: true,
        fullscreen: false,
        ..Default::default()
    }
}

#[macroquad::main(conf)]
async fn main() {
    day16::run().await;
}
