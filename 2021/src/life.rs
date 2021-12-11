use macroquad::prelude::*;
use rayon::iter::{IndexedParallelIterator, IntoParallelRefMutIterator, ParallelIterator};

use crate::utils::*;

#[derive(Copy, Clone, Debug, PartialEq, Eq)]
enum Cell {
    Alive,
    Dead,
}

pub async fn run() {
    // let resolution = 1000;
    let mut w = 1400;
    let mut h = 1400;

    let mut curr = vec![Cell::Dead; w * h];
    let mut next = vec![Cell::Dead; w * h];

    let image = Image::gen_image_color(w as u16, h as u16, BLACK);

    for c in &mut curr {
        if rand::gen_range(0, 5) as usize == 0 {
            *c = Cell::Alive;
        }
    }
    let mut zoom = vec2(1., screen_width() / screen_height());
    let mut target = vec2(20. * (w / 2) as f32, 20. * (h / 2) as f32);

    loop {
        clear_background(BLACK);
        set_camera(&Camera2D {
            zoom,
            target,
            ..Default::default()
        });
        w = image.width();
        h = image.height();
        if is_key_down(KeyCode::E) {
            zoom *= 1.1;
        }
        if is_key_down(KeyCode::Q) {
            zoom /= 1.1;
        }
        let mut key_rot = |key: KeyCode, v: (f32, f32)| {
            if is_key_down(key) {
                target = vec2(
                    target[0] + v.0 * 0.05 / zoom[0],
                    target[1] + v.1 * 0.06 / zoom[1],
                );
            }
        };
        key_rot(KeyCode::W, (0., 1.));
        key_rot(KeyCode::A, (-1., 0.));
        key_rot(KeyCode::S, (0., -1.));
        key_rot(KeyCode::D, (1., 0.));

        next.par_iter_mut().enumerate().for_each(|(i, c)| {
            let alive_neighbors = neighbors_flat(i, &(w as usize), &(h as usize))
                .map(|p| match &curr[p] {
                    Cell::Alive => 1,
                    Cell::Dead => 0,
                })
                .sum::<usize>();
            *c = match (&c, alive_neighbors) {
                (Cell::Dead, 3) => Cell::Alive,
                (Cell::Alive, 2) => Cell::Alive,
                (Cell::Alive, 3) => Cell::Alive,
                _ => Cell::Dead,
            };
        });

        for i in 0..next.len() {
            curr[i] = next[i];
            if next[i] == Cell::Alive {
                draw_rectangle(20. * (i / w) as f32, 20. * (i % w) as f32, 19., 19., WHITE);
            }
        }

        set_default_camera();
        draw_text(format!("{}", get_fps()).as_str(), 10.0, 20.0, 30.0, RED);
        next_frame().await
    }
}
