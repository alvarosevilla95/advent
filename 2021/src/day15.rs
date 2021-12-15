// https://adventofcode.com/2021/day/15

use array2d::Array2D;
use itertools::Itertools;
use macroquad::prelude::*;
use petgraph::{algo::dijkstra, graphmap::DiGraphMap};

use crate::utils::*;

pub async fn run() {
    let input = get_input(15).await;
    let _input = "1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581";

    let maze = input
        .lines()
        .map(|l| l.chars().map(|c| c.parse_i32() as usize).collect_vec())
        .collect_vec();
    let maze = Array2D::from_rows(&maze);

    let r_len = maze.row_len();
    let c_len = maze.column_len();
    let maze_iter = (0..5)
        .flat_map(move |x| {
            (0..r_len)
                .flat_map(move |i| (0..5).flat_map(move |y| (0..c_len).map(move |j| (x, y, i, j))))
        })
        .map(|(x, y, i, j)| (maze.get(i, j).unwrap() + x + y - 1) % 9 + 1);
    let maze = Array2D::from_iter_row_major(maze_iter, maze.row_len() * 5, maze.column_len() * 5);

    let mut graph = DiGraphMap::new();
    for i in 0..maze.row_len() {
        for j in 0..maze.column_len() {
            for (ii, jj, n) in neighbors_2d(&maze, (i, j), false, false) {
                graph.add_edge((i, j), (ii, jj), *n);
            }
        }
    }
    let path = dijkstra(&graph, (0, 0), Some((499, 499)), |e| *e.2);
    info!("{:?}", path.get(&(499, 499)));
    info!("{:?}", path.iter().map(|(_, v)| v).sum::<usize>());
}
