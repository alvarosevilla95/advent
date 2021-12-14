// https://adventofcode.com/2021/day/9

use itertools::Itertools;
use macroquad::prelude::*;

use crate::utils::*;

// If you can model how the smoke flows through the caves,
// you might be able to avoid it and be that much safer.
// The submarine generates a heightmap of the floor of
// the nearby caves for you (your puzzle input).
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

    // Part 1
    // Find all of the low points on your heightmap.
    // What is the sum of the risk levels of all low points on your heightmap?
    let local_mins = (0..row_len)
        .cartesian_product(0..col_len)
        .filter(|(i, j)| neighbors(&map, i, j).all(|(ii, jj)| map[*i][*j] < map[ii][jj]))
        .collect_vec();

    info!(
        "Sum of local minimums: {:?}",
        local_mins.iter().map(|(i, j)| map[*i][*j] + 1).sum::<i32>()
    );

    // Part 2
    // A basin is all locations that eventually flow downward to a single low point.
    // Find the three largest basins and multiply their sizes together.
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
                neighbors(&map, &i, &j).for_each(|n| {
                    let cc = map[n.0][n.1];
                    if visited.contains(&n) || cc == 9 || cc <= c {
                        return;
                    }
                    visited.push(n);
                    if cc >= c {
                        to_visit.push(n);
                    }
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
