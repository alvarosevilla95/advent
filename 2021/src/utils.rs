use array2d::Array2D;
use itertools::Itertools;
use macroquad::prelude::*;
use regex::Regex;

pub async fn get_input(day: usize) -> String {
    load_string(&format!("inputs/day{}.txt", day))
        .await
        .unwrap()
}

pub fn modulus<T>(a: T, b: T) -> T
where
    T: std::ops::Rem<Output = T> + std::ops::Add<Output = T> + Copy,
{
    ((a % b) + b) % b
}

pub fn neighbors_2d<T: Clone>(
    map: &Array2D<T>,
    (i, j): (usize, usize),
    warp: bool,
    include_diagonal: bool,
) -> impl Iterator<Item = (usize, usize, &T)> {
    let op = if include_diagonal {
        std::ops::BitOr::bitor
    } else {
        std::ops::BitXor::bitxor
    };
    [-1, 0, 1]
        .iter()
        .cartesian_product([-1, 0, 1].iter())
        .filter(move |(ii, jj)| {
            op(**ii != 0, **jj != 0)
                && (!(i == 0 && **ii == -1
                    || j == 0 && **jj == -1
                    || i == map.row_len() - 1 && **ii == 1
                    || j == map.column_len() - 1 && **jj == 1)
                    || warp)
        })
        .map(move |(ii, jj)| {
            (
                modulus(i as i32 + ii, map.row_len() as i32) as usize,
                modulus(j as i32 + jj, map.column_len() as i32) as usize,
            )
        })
        .map(|(i, j)| (i, j, map.get(i, j).unwrap()))
}

pub fn neighbors_flat(i: usize, columns: usize, rows: usize) -> impl Iterator<Item = usize> {
    let i = i as i32;
    let columns = columns as i32;
    let rows = rows as i32;
    [-1, 0, 1]
        .iter()
        .cartesian_product([-1, 0, 1].iter())
        .filter(move |(ii, jj)| {
            !((**ii == 0) && (**jj == 0))
                && !((i / columns == 0) && **ii == -1
                    || (i % columns == 0) && **jj == -1
                    || (i / columns == rows - 1) && **ii == 1
                    || (i % columns == columns - 1) && **jj == 1)
        })
        .map(move |(ii, jj)| (i + ii * rows + jj) as usize)
}

pub fn neighbors<'a, T>(
    map: &'a [Vec<T>],
    i: &'a usize,
    j: &'a usize,
) -> impl Iterator<Item = (usize, usize)> + 'a {
    [-1, 0, 1]
        .iter()
        .cartesian_product([-1, 0, 1].iter())
        .filter(|(ii, jj)| {
            ((**ii != 0) || (**jj != 0))
                && !(*i == 0 && **ii == -1
                    || *j == 0 && **jj == -1
                    || *i == map.len() - 1 && **ii == 1
                    || *j == map[0].len() - 1 && **jj == 1)
        })
        .map(|(ii, jj)| ((*i as i32 + *ii) as usize, (*j as i32 + *jj) as usize))
}

pub trait StringUtils {
    fn parse_i32(&self) -> i32;
}

impl StringUtils for str {
    fn parse_i32(&self) -> i32 {
        self.parse::<i32>().unwrap()
    }
}

impl StringUtils for char {
    fn parse_i32(&self) -> i32 {
        String::from(*self).parse::<i32>().unwrap()
    }
}

pub trait RegexUtils {
    fn is_match(&self, re: &str) -> bool;
    fn split_re(&self, re: &str) -> Vec<&str>;
}

impl RegexUtils for str {
    fn is_match(&self, re: &str) -> bool {
        Regex::new(re).unwrap().is_match(self)
    }

    fn split_re(&self, re: &str) -> Vec<&str> {
        Regex::new(re).unwrap().split(self).collect()
    }
}
