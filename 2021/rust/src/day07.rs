// https://adventofcode.com/2021/day/7

use crate::utils::*;
use itertools::Itertools;
use macroquad::prelude::*;

// Determine the horizontal position that the crabs can align to
// using the least fuel possible so they can make you an escape route!
// How much fuel must they spend to align to that position?
pub async fn run() {
    let crabs = get_input(7)
        .await
        .strip_suffix('\n')
        .unwrap()
        .split(',')
        .map(|f| f.parse_i32())
        .sorted()
        .collect::<Vec<i32>>();

    // Part 1
    let median = crabs[crabs.len() / 2 - 1];
    let total_fuel: i32 = crabs.iter().map(|c| (c - median).abs()).sum();
    info!("{} crabs. Total fuel is is {:?}", crabs.len(), total_fuel);

    // Part 2
    let average: i32 = crabs.iter().sum::<i32>() / crabs.len() as i32;
    let total_fuel: i32 = crabs
        .iter()
        .map(|c| (c - average).abs() * ((c - average).abs() + 1) / 2)
        .sum();
    info!("{} crabs. Total fuel is is {:?}", crabs.len(), total_fuel);
}
