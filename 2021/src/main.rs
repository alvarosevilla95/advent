#![feature(nll)]
#![feature(test)]
#![allow(dead_code)]

use macroquad::prelude::*;

// extern crate blas_src;
extern crate image;
extern crate lazy_static;

pub mod day1;
pub mod day2;
pub mod day3;
pub mod day4;
pub mod day5;
pub mod day6;
pub mod day7;
pub mod day8;
pub mod utils;

pub mod evolution;
pub mod graphics;
pub mod mandelbrot;

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
    day8::run().await;
}
