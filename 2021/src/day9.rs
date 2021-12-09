// https://adventofcode.com/2021/day/9

use std::option::Iter;

use itertools::Itertools;
use macroquad::prelude::*;

use crate::utils::{get_input, StringUtils};

pub async fn run() {
    let input = get_input(9).await;
    let _input = "2199943210
3987894921
9856789892
8767896789
9899965678";

    let map = input
        .lines()
        .map(|l| l.chars().map(|c| c.parse_i32()).collect_vec())
        .collect_vec();

    let row_len = map.len();
    let col_len = map[0].len();
    let surr = [-1, 0, 1];

    let mut local_mins = vec![];
    for i in 0..row_len {
        for j in 0..col_len {
            if surr
                .iter()
                .map(|ii| {
                    surr.iter()
                        .filter(|jj| {
                            (*ii == 0) ^ (**jj == 0)
                                && !(i == 0 && *ii == -1
                                    || j == 0 && **jj == -1
                                    || i == row_len - 1 && *ii == 1
                                    || j == col_len - 1 && **jj == 1)
                        })
                        .all(|jj| {
                            map[i][j] < map[(i as i32 + *ii) as usize][(j as i32 + *jj) as usize]
                        })
                })
                .all(|b| b)
            {
                local_mins.push((i, j));
            }
        }
    }
    info!(
        "Sum of local minimums: {:?}",
        local_mins.iter().map(|(i, j)| map[*i][*j] + 1).sum::<i32>()
    );

    let basins = local_mins
        .iter()
        .map(|(i, j)| {
            let mut visited: Vec<(usize, usize)> = Vec::new();
            let mut to_visit: Vec<(usize, usize)> = Vec::new();
            visited.push((*i, *j));
            to_visit.push((*i, *j));
            while !to_visit.is_empty() {
                let (i, j) = to_visit.pop().unwrap();
                let c = map[i][j];
                surr.iter().for_each(|ii| {
                    surr.iter()
                        .filter(|jj| {
                            (*ii == 0) ^ (**jj == 0)
                                && !(i == 0 && *ii == -1
                                    || j == 0 && **jj == -1
                                    || i == row_len - 1 && *ii == 1
                                    || j == col_len - 1 && **jj == 1)
                        })
                        .for_each(|jj| {
                            let n = ((i as i32 + *ii) as usize, (j as i32 + *jj) as usize);
                            let cc = map[(i as i32 + *ii) as usize][(j as i32 + *jj) as usize];
                            if visited.contains(&n) || cc == 9 || cc <= c {
                                return;
                            }
                            visited.push(n);
                            if cc >= c {
                                to_visit.push(n);
                            }
                        })
                });
            }
            visited
        })
        .collect_vec();

    let top_product: usize = basins
        .iter()
        .map(|b| b.len())
        .sorted()
        .rev()
        .take(3)
        .product();

    info!("Product of 3 largest basins: {:?}", top_product);
}
