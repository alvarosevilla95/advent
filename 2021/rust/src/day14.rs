// https://adventofcode.com/2021/day/14

use std::collections::HashMap;

use itertools::Itertools;
use macroquad::prelude::*;

use crate::utils::*;

// The first line is the polymer template - this is the starting point of the process.
// The following section defines the pair insertion rules. A rule like AB -> C means
// that when elements A and B are immediately adjacent, element C should be inserted
// between them. These insertions all happen simultaneously.
//
// Part 1
// Apply 10 steps of pair insertion to the polymer template and find the most and least
// common elements in the result. What do you get if you take the quantity of the most
// common element and subtract the quantity of the least common element?
//
// Part 2
// Apply 40 steps of pair insertion
pub async fn run() {
    let input = get_input(14).await;
    let _input = "NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C";

    let polymer = input.lines().next().unwrap();
    let map = input
        .lines()
        .skip(2)
        .map(|l| l.split(" -> ").collect_tuple().unwrap())
        .map(|(k, v)| {
            (
                k,
                (
                    k.get(0..1).unwrap().to_owned() + v,
                    v.to_owned() + k.get(1..2).unwrap(),
                ),
            )
        })
        .collect::<HashMap<&str, (String, String)>>();

    let mut eles = HashMap::new();
    let mut pairs = HashMap::new();
    eles.insert(polymer.get(0..1).unwrap(), 1);
    for i in 1..polymer.len() {
        *eles.entry(polymer.get(i..i + 1).unwrap()).or_insert(0) += 1;
        let pair = polymer.get(i - 1..i + 1).unwrap();
        if map.contains_key(pair) {
            *pairs.entry(pair).or_insert(0) += 1;
        }
    }

    for _ in 0..40 {
        let mut new_pairs = HashMap::new();
        for (k, v) in &pairs {
            let (p1, p2) = map.get(k).unwrap();
            *new_pairs.entry(p1.as_str()).or_insert(0) += v;
            *new_pairs.entry(p2.as_str()).or_insert(0) += v;
            *eles.entry(p1.get(1..2).unwrap()).or_insert(0) += v;
        }
        pairs = new_pairs.clone();
    }

    let sorted = eles.iter().map(|(_, v)| v).sorted().collect_vec();
    info!("{:?}", eles.values().sum::<i64>());
    info!("{:?}", sorted[sorted.len() - 1] - sorted[0]);
}
