#![feature(nll)]
#![feature(test)]
#![allow(dead_code)]

use macroquad::prelude::*;

extern crate image;

pub mod day1;
pub mod day10;
pub mod day11;
pub mod day12;
pub mod day13;
pub mod day2;
pub mod day3;
pub mod day4;
pub mod day5;
pub mod day6;
pub mod day7;
pub mod day8;
pub mod day9;
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
    day13::run().await;
}
