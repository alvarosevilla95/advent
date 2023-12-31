// https://adventofcode.com/2021/day/12

use itertools::Itertools;
use macroquad::prelude::*;
use petgraph::graphmap::UnGraphMap;

use crate::utils::get_input;

// Your goal is to find the number of distinct paths that start at start, end at end,
// and don't visit small caves more than once. There are two types of caves:
// big caves (written in uppercase, like A) and small caves (written in lowercase, like b).
pub async fn run() {
    let input = get_input(12).await;
    let _input = "dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc";

    let parsed = input
        .lines()
        .map(|l| l.split('-').collect_tuple::<(&str, &str)>().unwrap());
    let graph = UnGraphMap::from_edges(parsed);

    // Part 1
    // How many paths through this cave system are there that visit small caves at most once?
    let paths = search(&graph, &["start"], 0);
    info!("{:?}", paths.len());

    // Part 2
    // After reviewing the available paths, you realize you might have time to visit a single small cave twice.
    // Specifically, big caves can be visited any number of times, a single small cave can be visited at
    // most twice, and the remaining small caves can be visited at most once.
    // However, the caves named start and end can only be visited exactly once each
    let paths = search(&graph, &["start"], 1);
    info!("{:?}", paths.len());
}

fn search<'a>(
    graph: &UnGraphMap<&'a str, i32>,
    path: &[&'a str],
    max_small_visits: usize,
) -> Vec<Vec<&'a str>> {
    let last = path[path.len() - 1];
    if last == "end" {
        let mut new_path = path.to_vec();
        new_path.push("end");
        return vec![new_path.to_vec()];
    }
    let is_small = |n: &str| n.chars().all(|c| c.is_lowercase());
    graph
        .neighbors(last)
        .flat_map(|node| {
            if node == "start"
                || node == last
                || is_small(node)
                    && path.contains(&node)
                    && path
                        .iter()
                        .filter(|n| is_small(n))
                        .sorted()
                        .group_by(|c| *c)
                        .into_iter()
                        .any(|(_, v)| v.count() > max_small_visits)
            {
                vec![]
            } else {
                let mut new_path = path.to_vec();
                new_path.push(node);
                search(graph, &new_path, max_small_visits)
            }
        })
        .collect_vec()
}
