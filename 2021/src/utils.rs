use macroquad::prelude::*;

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
