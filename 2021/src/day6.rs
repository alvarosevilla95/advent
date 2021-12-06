// https://adventofcode.com/2021/day/6

use std::collections::HashMap;

use crate::utils::*;
use macroquad::prelude::*;
use ndarray::{arr2, Array, Array2, Dim};

// Find a way to simulate lanternfish.
// How many lanternfish would there be after 80 days?
pub async fn run() {
    let _input = "3,4,3,1,2";
    let input = get_input(6).await;
    let mut fish = parse_fish(&input);
    iterate_fish_stochastic(&mut fish, 420);
    info!("Total fish: {}", fish.values().sum::<i64>(),);
    info!("Current schedule: {:?}", fish);
}

fn parse_fish(input: &str) -> HashMap<i32, i64> {
    let mut fish = HashMap::new();
    for i in 0..9 {
        fish.insert(i, 0 as i64);
    }

    input
        .strip_suffix('\n')
        .unwrap()
        .split(',')
        .map(|f| f.parse_i32())
        .for_each(|f| {
            *fish.get_mut(&f).unwrap() += 1;
        });

    fish
}

fn iterate_fish(fish: &mut HashMap<i32, i64>, time: i32) {
    for _ in 0..time {
        let b = fish.remove(&0).unwrap();
        for f in 0..8 {
            let c = fish.remove(&(f + 1)).unwrap();
            fish.insert(f, c);
        }
        fish.insert(8, b);
        *fish.get_mut(&6).unwrap() += b;
    }
}

fn iterate_fish_stochastic(raw_fish: &mut HashMap<i32, i64>, time: i32) {
    fn euler_exp(m: &Array2<i64>, e: i32) -> Array2<i64> {
        match e {
            1 => m.to_owned(),
            e if e % 2 == 0 => euler_exp(&(m * m), e / 2),
            _ => euler_exp(m, (e - 1) / 2) * m,
        }
    }

    let mut fish: Array<i64, Dim<[usize; 1]>> = Array::zeros(9);
    for (i, v) in raw_fish.iter() {
        *fish.get_mut(*i as usize).unwrap() = *v;
    }
    let m: Array2<i64> = arr2(&[
        [0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
    ]);
    let m = euler_exp(&m, 256);
    let fish = m.dot(&fish);
    for (i, v) in fish.iter().enumerate() {
        *raw_fish.get_mut(&(i as i32)).unwrap() = *v;
    }
}

extern crate test;

#[cfg(test)]
mod tests {
    use super::iterate_fish;
    use super::parse_fish;
    use super::test::Bencher;

    #[bench]
    fn bench_exponential_fish(b: &mut Bencher) {
        let input = "1,1,1,1,2,1,1,4,1,4,3,1,1,1,1,1,1,1,1,4,1,3,1,1,1,5,1,3,1,4,1,2,1,1,5,1,1,1,1,1,1,1,1,1,1,3,4,1,5,1,1,1,1,1,1,1,1,1,3,1,4,1,1,1,1,3,5,1,1,2,1,1,1,1,4,4,1,1,1,4,1,1,4,2,4,4,5,1,1,1,1,2,3,1,1,4,1,5,1,1,1,3,1,1,1,1,5,5,1,2,2,2,2,1,1,2,1,1,1,1,1,3,1,1,1,2,3,1,5,1,1,1,2,2,1,1,1,1,1,3,2,1,1,1,4,3,1,1,4,1,5,4,1,4,1,1,1,1,1,1,1,1,1,1,2,2,4,5,1,1,1,1,5,4,1,3,1,1,1,1,4,3,3,3,1,2,3,1,1,1,1,1,1,1,1,2,1,1,1,5,1,3,1,4,3,1,3,1,5,1,1,1,1,3,1,5,1,2,4,1,1,4,1,4,4,2,1,2,1,3,3,1,4,4,1,1,3,4,1,1,1,2,5,2,5,1,1,1,4,1,1,1,1,1,1,3,1,5,1,2,1,1,1,1,1,4,4,1,1,1,5,1,1,5,1,2,1,5,1,1,1,1,1,1,1,1,1,1,1,1,3,2,4,1,1,2,1,1,3,2\n";
        let mut fish = parse_fish(input);
        b.iter(|| {
            iterate_fish(&mut fish, 420);
        });
    }

    #[bench]
    fn bench_exponential_fish_stochastic(b: &mut Bencher) {
        let input = "1,1,1,1,2,1,1,4,1,4,3,1,1,1,1,1,1,1,1,4,1,3,1,1,1,5,1,3,1,4,1,2,1,1,5,1,1,1,1,1,1,1,1,1,1,3,4,1,5,1,1,1,1,1,1,1,1,1,3,1,4,1,1,1,1,3,5,1,1,2,1,1,1,1,4,4,1,1,1,4,1,1,4,2,4,4,5,1,1,1,1,2,3,1,1,4,1,5,1,1,1,3,1,1,1,1,5,5,1,2,2,2,2,1,1,2,1,1,1,1,1,3,1,1,1,2,3,1,5,1,1,1,2,2,1,1,1,1,1,3,2,1,1,1,4,3,1,1,4,1,5,4,1,4,1,1,1,1,1,1,1,1,1,1,2,2,4,5,1,1,1,1,5,4,1,3,1,1,1,1,4,3,3,3,1,2,3,1,1,1,1,1,1,1,1,2,1,1,1,5,1,3,1,4,3,1,3,1,5,1,1,1,1,3,1,5,1,2,4,1,1,4,1,4,4,2,1,2,1,3,3,1,4,4,1,1,3,4,1,1,1,2,5,2,5,1,1,1,4,1,1,1,1,1,1,3,1,5,1,2,1,1,1,1,1,4,4,1,1,1,5,1,1,5,1,2,1,5,1,1,1,1,1,1,1,1,1,1,1,1,3,2,4,1,1,2,1,1,3,2\n";
        let mut fish = parse_fish(input);
        b.iter(|| {
            iterate_fish(&mut fish, 420);
        });
    }
}
