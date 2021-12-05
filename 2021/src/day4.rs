// https://adventofcode.com/2021/day/3

use macroquad::prelude::*;
use nalgebra::Vector5;
use std::collections::HashMap;

use crate::utils::*;

// To guarantee victory against the giant squid, figure out which board will win first.
// What will your final score be if you choose that board?
//
// Figure out which board will win last. Once it wins, what would its final score be?
pub async fn run() {
    let input = get_input(4).await;

    let rng = input
        .lines()
        .next()
        .unwrap()
        .split(',')
        .map(|s| s)
        .map(|s| s.parse::<i32>().unwrap());

    let mut boards = input
        .lines()
        .skip(1)
        .enumerate()
        .fold(Vec::new(), |mut boards, (i, line)| {
            if i % 6 == 0 {
                boards.push(Board::default());
            } else {
                let len = boards.len();
                let row = line.split_whitespace().map(|s| s.parse::<i32>().unwrap());
                row.enumerate().for_each(|(j, r)| {
                    boards
                        .get_mut(len - 1)
                        .unwrap()
                        .entries
                        .insert(r, (i % 6 - 1, j, false));
                });
            }
            boards
        });

    let mut winners = 0;
    let total = boards.len();
    'outer: for r in rng {
        for b in boards.iter_mut().filter(|b| !b.won()) {
            winners += b.tick(r) as usize;
            let part_1 = |w: usize| w == 1;
            let part_2 = |w: usize| w == total;
            if part_2(winners) {
                let sum = b.score();
                info!("Found winner");
                b.print();
                info!("Last: {}, Sum: {}, Score: {}", r, sum, r * sum);
                break 'outer;
            }
        }
    }
}

#[derive(Default)]
struct Board {
    entries: HashMap<i32, (usize, usize, bool)>,
    row_scores: Vector5<i32>,
    column_scores: Vector5<i32>,
}

impl Board {
    fn won(&self) -> bool {
        self.row_scores.iter().any(|i| *i == 5) || self.column_scores.iter().any(|i| *i == 5)
    }

    fn tick(&mut self, r: i32) -> bool {
        let entries = self.entries.to_owned();
        entries
            .get(&r)
            .map(|e| (e, self.row_scores[e.0] + 1, self.column_scores[e.1] + 1))
            .map(|(e, s, v)| {
                self.entries.insert(r, (e.0, e.1, true));
                std::mem::replace(&mut self.row_scores[e.0], s);
                std::mem::replace(&mut self.column_scores[e.1], v);
                self.won()
            })
            .unwrap_or_else(|| false)
    }

    fn score(&self) -> i32 {
        self.entries
            .iter()
            .filter(|(k, v)| !v.2)
            .map(|(k, v)| k)
            .sum::<i32>()
    }

    fn print(&self) {
        info!("Board");
        for i in 0..5 {
            let row = (0..5)
                .map(|j| {
                    self.entries
                        .iter()
                        .find(move |(k, v)| (v.0, v.1) == (i, j))
                        .map(|(k, v)| (k, v.2))
                        .unwrap()
                })
                .collect::<Vec<(&i32, bool)>>();
            info!("{:?}", row);
        }
        info!("Row scores: {:?}", self.row_scores.as_slice());
        info!("Column scores: {:?}", self.column_scores.as_slice());
    }
}
