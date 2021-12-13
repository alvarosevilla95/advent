// https://adventofcode.com/2021/day/3

use macroquad::prelude::*;
use std::collections::BTreeMap;

use crate::utils::*;

pub async fn run() {
    let input = get_input(3).await;
    let _input = "00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010";

    let signals = input
        .lines()
        .map(|l| usize::from_str_radix(l, 2).unwrap().try_into().unwrap())
        .collect::<Vec<i32>>();
    part_1(&(signals.clone()));
    part_2(&signals);
}

// Use the binary numbers in your diagnostic report to calculate the gamma rate and epsilon rate,
// then multiply them together. What is the power consumption of the submarine?
fn part_1(signals: &[i32]) {
    let gamma = (0..12)
        .map(|i| signals.iter().map(|s| s.bit_at(i)).filter(|b| *b).count() * 2 >= signals.len())
        .enumerate()
        .fold(0, |acc, n| {
            n.1 as i32 * i32::pow(2, n.0.try_into().unwrap()) + acc
        });
    let epsilon = gamma ^ 0xFFF;
    info!(
        "gamma: {}, epsilon: {}, product: {}",
        gamma,
        epsilon,
        gamma * epsilon
    );
}

// Use the binary numbers in your diagnostic report to calculate the oxygen generator rating
// and CO2 scrubber rating, then multiply them together. What is the life support rating of the submarine?
fn part_2(signals: &[i32]) {
    let find = |reverse: bool| -> i32 {
        let mut candidates = signals.to_vec();
        for i in (0..12).rev() {
            let significant_bit = candidates
                .iter()
                .map(|c| c.bit_at(i))
                .filter(|b| *b)
                .count()
                * 2
                >= candidates.len();
            candidates = candidates
                .into_iter()
                .filter(|c| (c.bit_at(i) == significant_bit) == reverse)
                .collect();
            if candidates.len() == 1 {
                break;
            }
        }
        *candidates.get(0).unwrap()
    };

    let oxygen = find(false);
    let co2 = find(true);
    info!(
        "oxygen: {}, co2: {}, product: {}",
        oxygen,
        co2,
        oxygen * co2
    );
}

trait Bitmap {
    fn bit_at(&self, i: usize) -> bool;
}

impl Bitmap for i32 {
    fn bit_at(&self, i: usize) -> bool {
        ((self >> i) & 1) == 1
    }
}

fn most_frequent(list: Vec<bool>) -> bool {
    list.iter().filter(|b| **b).count() * 2 >= list.len()
}
