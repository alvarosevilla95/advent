// https://adventofcode.com/2021/day/10

use crate::utils::*;
use itertools::Itertools;
use macroquad::prelude::*;

// The navigation subsystem syntax is made of several lines containing chunks.
// There are one or more chunks on each line, and chunks contain zero or more other chunks.
// Adjacent chunks are not separated by any delimiter; if one chunk stops, the next chunk (if any) can
// immediately start. Every chunk must open and close with one of four legal pairs of matching character
pub async fn run() {
    let _input = "[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]";
    let input = get_input(10).await;

    fn complete_line(line: &str) -> Result<String, usize> {
        let mut stack = vec![];
        for c in line.chars() {
            match c {
                '(' => stack.push(')'),
                '[' => stack.push(']'),
                '{' => stack.push('}'),
                '<' => stack.push('>'),
                ')' if stack.pop().unwrap() != ')' => return Err(3),
                ']' if stack.pop().unwrap() != ']' => return Err(57),
                '}' if stack.pop().unwrap() != '}' => return Err(1197),
                '>' if stack.pop().unwrap() != '>' => return Err(25137),
                _ => (),
            }
        }
        Ok(stack.iter().rev().join(""))
    }

    // Part 1
    // Find the first illegal character in each corrupted line of the navigation subsystem.
    // What is the total syntax error score for those errors?
    let corrupted = input.lines().map(complete_line).flat_map(Result::err);
    info!("Corrupted Score: {}", corrupted.sum::<usize>());

    // Part 2
    // Find the completion string for each incomplete line, score the completion strings,
    // and sort the scores. What is the middle score?
    let completed = input
        .lines()
        .flat_map(complete_line)
        .map(|l| {
            l.chars().fold(0_i64, |acc, c| match c {
                ')' => 5 * acc + 1,
                ']' => 5 * acc + 2,
                '}' => 5 * acc + 3,
                '>' => 5 * acc + 4,
                _ => panic!(),
            })
        })
        .sorted()
        .collect_vec();

    info!(
        "Median Completion Score: {:?}",
        completed[completed.len() / 2]
    );
}
