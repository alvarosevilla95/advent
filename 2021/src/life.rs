use macroquad::prelude::*;
use rayon::iter::{IndexedParallelIterator, IntoParallelRefMutIterator, ParallelIterator};

use crate::{utils::*, world2d::World2D};

#[derive(Copy, Clone, Debug, PartialEq, Eq)]
enum Cell {
    Alive,
    Dead,
}

pub async fn run() {
    let w = 1400;
    let h = 1400;
    let mut curr = vec![Cell::Dead; w * h];
    let mut next = vec![Cell::Dead; w * h];
    let mut canvas = World2D::from_world(
        w,
        h,
        |c| match c {
            Cell::Alive => WHITE,
            Cell::Dead => BLACK,
        },
        BLACK,
    );

    for c in &mut curr {
        if rand::gen_range(0, 5) as usize == 0 {
            *c = Cell::Alive;
        }
    }

    loop {
        next.par_iter_mut().enumerate().for_each(|(i, c)| {
            let alive_neighbors = neighbors_flat(i, w as usize, h as usize)
                .map(|p| match &curr[p] {
                    Cell::Alive => 1,
                    Cell::Dead => 0,
                })
                .sum::<usize>();
            *c = match (&c, alive_neighbors) {
                (Cell::Dead, 3) => Cell::Alive,
                (Cell::Alive, 3) => Cell::Alive,
                (Cell::Alive, 2) => Cell::Alive,
                _ => Cell::Dead,
            };
        });
        curr = next.clone();
        canvas.draw(&curr, 1).await;
    }
}
