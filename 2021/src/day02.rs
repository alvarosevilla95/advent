// https://adventofcode.com/2021/day/2

use crate::utils::*;
use macroquad::prelude::*;

#[derive(Debug, Clone)]
enum Direction {
    Up,
    Down,
    Forward,
}

#[derive(Clone)]
struct Instruction {
    direction: Direction,
    amount: i32,
}

#[derive(Debug)]
struct Position {
    aim: i32,
    x: i32,
    y: i32,
}

// Calculate the horizontal position and depth you would have after following the planned course.
// What do you get if you multiply your final horizontal position by your final depth?
pub async fn run() {
    let instructions = get_input(2)
        .await
        .lines()
        .map(|line| line.split(' ').collect())
        .map(|pair: Vec<&str>| Instruction {
            direction: match *pair.get(0).unwrap() {
                "up" => Direction::Up,
                "down" => Direction::Down,
                "forward" => Direction::Forward,
                _ => panic!("couldn't parse"),
            },
            amount: pair.get(1).unwrap().parse_i32(),
        })
        .collect::<Vec<Instruction>>();
    part_1(&instructions);
    part_2(&instructions);
}

fn part_1(instructions: &[Instruction]) {
    let position = instructions
        .iter()
        .fold(Position { aim: 0, x: 0, y: 0 }, |pos, l| {
            match &l.direction {
                Direction::Up => Position {
                    y: pos.y - l.amount,
                    ..pos
                },
                Direction::Down => Position {
                    y: pos.y + l.amount,
                    ..pos
                },
                Direction::Forward => Position {
                    x: pos.x + l.amount,
                    ..pos
                },
            }
        });
    info!("Part 1");
    info!("{:?}", position);
    info!("{:?}", position.x * position.y);
}

fn part_2(instructions: &[Instruction]) {
    let position = instructions
        .iter()
        .fold(Position { aim: 0, x: 0, y: 0 }, |pos, l| {
            match &l.direction {
                Direction::Up => Position {
                    aim: pos.aim - l.amount,
                    ..pos
                },
                Direction::Down => Position {
                    aim: pos.aim + l.amount,
                    ..pos
                },
                Direction::Forward => Position {
                    x: pos.x + l.amount,
                    y: pos.y + l.amount * pos.aim,
                    ..pos
                },
            }
        });
    info!("Part 2");
    info!("{:?}", position);
    info!("{:?}", position.x * position.y);
}
