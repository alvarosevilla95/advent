// https://adventofcode.com/2021/day/11

use crate::{utils::*, world2d::World2D};
use itertools::Itertools;
use macroquad::prelude::*;

pub async fn run() {
    let _input = "5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526";
    let input = get_input(11).await;
    let mut map = input
        .lines()
        .map(|l| l.chars().map(|c| c.parse_i32()).collect_vec())
        .collect_vec();

    let mut total = 0;
    let mut canvas = World2D::from_world(
        map.len(),
        map[0].len(),
        |c| match *c {
            0 => WHITE,
            i => Color::new(i as f32 / 50., i as f32 / 50., i as f32 / 50., 1.0),
        },
        BLACK,
    );

    for i in 0..1000000 {
        let mut visited = vec![];
        for i in 0..map.len() {
            for j in 0..map[0].len() {
                total += flash(&mut visited, &mut map, i, j);
            }
        }
        visited.iter().for_each(|(i, j)| map[*i][*j] = 0);
        if i == 100 {
            info!("Flashes after 100 iterations: {}", total);
        }
        if visited.len() == map.len() * map[0].len() {
            info!("First iteration where all flashed: {}", i);
            break;
        }

        let flat = map.iter().flat_map(|c| c.iter()).copied().collect_vec();
        canvas.draw(&flat, 10).await;
    }
}

fn flash(visited: &mut Vec<(usize, usize)>, chars: &mut Vec<Vec<i32>>, i: usize, j: usize) -> i32 {
    chars[i][j] += 1;
    if chars[i][j] <= 9 || visited.contains(&(i, j)) {
        return 0;
    }
    visited.push((i, j));
    neighbors(chars, &i, &j)
        .collect_vec()
        .iter()
        .map(|(ii, jj)| flash(visited, chars, *ii, *jj))
        .sum::<i32>()
        + 1
}
