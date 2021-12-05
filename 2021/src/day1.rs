// https://adventofcode.com/2021/day/1

use crate::utils::*;
use macroquad::prelude::*;

pub async fn run() {
    let lines = get_input(1)
        .await
        .lines()
        .map(|x| x.parse_i32())
        .collect::<Vec<i32>>();
    part_1(&lines).await;
    part_2(&lines).await;
}

struct Acc {
    result: i32,
    last: i32,
}

// How many measurements are larger than the previous measurement?
async fn part_1(lines: &Vec<i32>) {
    let count = lines.into_iter().fold(
        Acc {
            result: 0,
            last: i32::MAX,
        },
        |acc, a| Acc {
            last: *a,
            result: if a > &acc.last {
                acc.result + 1
            } else {
                acc.result
            },
        },
    );
    info!("Part 1");
    info!("{}", count.result);
}

// Consider sums of a three-measurement sliding window. How many sums are larger than the previous sum?
async fn part_2(lines: &Vec<i32>) {
    let mut last_sum = i32::MAX;
    let mut total = 0;
    for i in 0..lines.len() - 2 {
        let sum = lines.get(i).unwrap() + lines.get(i + 1).unwrap() + lines.get(i + 2).unwrap();
        if sum > last_sum {
            total += 1
        }
        last_sum = sum;
    }
    info!("Part 2");
    info!("{}", total);
}
