// https://adventofcode.com/2021/day/8

use std::collections::{HashMap, HashSet};

use itertools::Itertools;
use macroquad::prelude::*;

use crate::utils::{get_input, StringUtils};

// For each entry, determine all of the wire/segment
// connections and decode the four-digit output values.
// What do you get if you add up all of the output values?
pub async fn run() {
    let _input =
        "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce";
    let input = get_input(8).await;

    let parse_line = |l: &str| {
        l.split(" | ")
            .map(|s| s.split(' ').map(|p| p.chars().collect()).collect_vec())
            .collect_vec()
    };
    let parsed = input.lines().map(parse_line).collect_vec();
    let is_base = |c: &&HashSet<char>| c.len() == 2 || c.len() == 3 || c.len() == 4 || c.len() == 7;

    // Part 1
    let cnt = parsed
        .iter()
        .flat_map(|r| r[1].iter().filter(&is_base))
        .count();
    info!("Count of (1, 4, 7, 8) in output: {}", cnt);

    // Part 2
    let by_count = parsed.iter().map(|r| {
        r[0].iter()
            .filter(is_base)
            .map(|c| (c.len(), c))
            .collect::<HashMap<usize, &HashSet<char>>>()
    });

    let decode = |n| match n {
        (2, _, _) => "1",
        (4, _, _) => "4",
        (3, _, _) => "7",
        (7, _, _) => "8",
        (5, _, 2) => "2",
        (5, 2, _) => "3",
        (5, _, _) => "5",
        (6, _, 4) => "9",
        (6, 2, _) => "0",
        (6, _, _) => "6",
        _ => panic!("Couldn't decode number {:?}", n),
    };

    let total: i32 = parsed
        .iter()
        .zip(by_count)
        .map(|(i, cnt)| {
            i[1].iter()
                .map(|n| {
                    decode((
                        n.len(),
                        n.intersection(&cnt.get(&2).unwrap()).count(),
                        n.intersection(&cnt.get(&4).unwrap()).count(),
                    ))
                })
                .join("")
                .parse_i32()
        })
        .sum();
    info!("Sum of parsed outputs: {:?}", total);
}
