#![feature(nll)]
#[allow(dead_code)]
use macroquad::prelude::*;

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
async fn main() {}
