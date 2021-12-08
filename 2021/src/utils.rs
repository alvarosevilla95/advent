use macroquad::prelude::*;
use regex::Regex;

pub async fn get_input(day: usize) -> String {
    load_string(&format!("inputs/day{}.txt", day))
        .await
        .unwrap()
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
