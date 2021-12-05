#![feature(nll)]
#[allow(dead_code)]
use macroquad::prelude::*;

pub mod utils;
// mod day1;
// mod day2;
// mod day3;
mod day4;

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
    day4::run().await;
}
