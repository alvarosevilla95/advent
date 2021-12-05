#[allow(dead_code)]
use macroquad::prelude::*;
use rand::gen_range;
use rstar::{PointDistance, RTree, RTreeObject, AABB};
use std::collections::HashSet;

const LETTERS: &[char] = &['a', 'd', 'p', 'm', 'n', 'n', 'n', 'i'];

fn random_gene() -> char {
    LETTERS[gen_range(0, LETTERS.len() as u32) as usize]
}

pub async fn run() {
    rand::srand(miniquad::date::now().to_bits());
    let mut biots = BiotCollection::new(500);

    loop {
        biots.step();
        clear_background(Color::new(0., 0., 0.1, 1.0));
        biots.draw();
        draw_text(
            &format!("FPS: {}, biots: {}", get_fps(), biots.len()),
            screen_width() - 250.,
            screen_height() - 5.,
            28.,
            LIGHTGRAY,
        );
        next_frame().await
    }
}

pub struct BiotCollection {
    biots: Vec<Biot>,
}

impl BiotCollection {
    pub fn new(n: usize) -> Self {
        Self {
            biots: (0..n).map(|_i| Biot::random_new()).collect(),
        }
    }

    pub fn step(&mut self) {
        let mut new: Vec<Biot> = Vec::new();
        let tree: RTree<TreePoint> = RTree::bulk_load(
            self.biots
                .iter()
                .enumerate()
                .map(|(n, biot)| TreePoint {
                    x: biot.pos.x,
                    y: biot.pos.y,
                    idx: n,
                })
                .collect(),
        );

        for n in 0..(self.biots.len()) {
            let mut feed_dir: Option<Vec2> = None;
            let biot = &self.biots[n];
            if self.biots[n].intelligence > 0. {
                let neighbors = tree
                    .nearest_neighbor_iter_with_distance_2(&[biot.pos.x as f64, biot.pos.y as f64]);
                for (other, d2) in neighbors {
                    if other.idx == n {
                        continue;
                    }
                    if d2 as f32 > (biot.intelligence.powf(2.)) * 1600. {
                        break;
                    }
                    if biot.stronger(&self.biots[other.idx]) {
                        feed_dir = Some(
                            vec2(
                                other.x as f32 - self.biots[n].pos.x,
                                other.y as f32 - self.biots[n].pos.y,
                            )
                            .normalize(),
                        );
                        break;
                    }
                }
            }
            self.biots[n]
                .step(&tree, feed_dir)
                .filter(|_v| self.biots.len() < 4000)
                .map(|offspring| new.push(offspring));
        }

        let mut visited: HashSet<usize> = HashSet::new();
        for f in tree.iter() {
            visited.insert(f.idx);
            for s in tree.locate_within_distance([f.x as f64, f.y as f64], 100.) {
                if !visited.contains(&s.idx) {
                    Biot::interact(&mut self.biots, f.idx, s.idx);
                }
            }
        }
        self.biots.retain(|b| !b.dead());
        self.biots.append(&mut new);
    }

    pub fn draw(&self) {
        self.biots.iter().for_each(|b| b.draw())
    }

    pub fn len(&self) -> usize {
        self.biots.len()
    }
}

#[derive(Clone, Debug)]
pub struct Biot {
    life: f32,
    pub pos: Vec2,
    speed: Vec2,
    age: u32,

    genome: Vec<char>,
    pub attack: f32,
    pub defense: f32,
    pub photosynthesis: f32,
    pub motion: f32,
    pub intelligence: f32,
}

impl Biot {
    pub fn random_new() -> Self {
        let genome = (0..13).map(|_i| random_gene()).collect();
        let mut s = Self {
            life: 0.,
            pos: vec2(
                gen_range(0., 1.) * screen_width(),
                gen_range(0., 1.) * screen_height(),
            ),
            speed: vec2(0., 0.),
            age: 0,
            genome,
            attack: 0.,
            defense: 0.,
            photosynthesis: 0.,
            motion: 0.,
            intelligence: 0.,
        };
        s.set_from_genome();
        s.life = s.base_life();
        s
    }

    pub fn step(&mut self, rtree: &RTree<TreePoint>, feed_dir: Option<Vec2>) -> Option<Biot> {
        let mut offspring = None;
        let adult_factor = 4.;
        if self.life >= self.base_life() * adult_factor {
            let close_by = rtree
                .nearest_neighbor_iter_with_distance_2(&[self.pos.x as f64, self.pos.y as f64])
                .nth(5);
            if close_by.map_or(true, |(_, d2)| d2 > 200.) {
                let mut off = self.clone();
                off.age = 0;
                while gen_range(0., 1.) < 0.2 {
                    off.mutate();
                }
                off.life = off.base_life();
                off.random_move(1.5);
                offspring = Some(off);
                self.life = (adult_factor - 1.) * self.base_life();
            }
        }
        self.pos += self.speed;
        self.pos.x = modulus(self.pos.x, screen_width());
        self.pos.y = modulus(self.pos.y, screen_height());
        self.speed *= 0.9;
        self.life += (self.photosynthesis - self.metabolism()) * 0.4;
        if gen_range(0., 1.) < 0.2 * self.motion {
            let speed = 7. * self.motion / self.weight();
            if self.intelligence > 0. {
                if let Some(feed_dir) = feed_dir {
                    self.accelerate(feed_dir, speed);
                } else {
                    self.random_move(speed)
                }
            } else {
                self.random_move(speed)
            }
        }
        self.age += 1;
        offspring
    }

    pub fn interact(biots: &mut Vec<Self>, i: usize, j: usize) {
        let dist = (biots[i].pos - biots[j].pos).length();
        if dist < 10. * (biots[i].weight() + biots[j].weight()) {
            if biots[i].stronger(&biots[j]) {
                biots[i].life += biots[j].life * 0.8;
                biots[j].life = 0.;
            } else if biots[j].stronger(&biots[i]) {
                biots[j].life += biots[i].life * 0.8;
                biots[i].life = 0.;
            }
        }
    }

    pub fn dead(&self) -> bool {
        self.life <= 0. || self.age >= 10000
    }

    pub fn stronger(&self, other: &Self) -> bool {
        self.attack > other.attack + other.defense * 0.9
    }

    fn set_from_genome(&mut self) {
        self.attack = self.genome.iter().filter(|&&c| c == 'a').count() as f32 * 0.1;
        self.defense = self.genome.iter().filter(|&&c| c == 'd').count() as f32 * 0.1;
        self.photosynthesis = self.genome.iter().filter(|&&c| c == 'p').count() as f32 * 0.1;
        self.motion = self.genome.iter().filter(|&&c| c == 'm').count() as f32 * 0.1;
        self.intelligence = self.genome.iter().filter(|&&c| c == 'i').count() as f32 * 10.;
    }

    fn random_move(&mut self, speed: f32) {
        self.accelerate(
            vec2(gen_range(-0.5, 0.5), gen_range(-0.5, 0.5)).normalize(),
            speed,
        );
    }

    fn accelerate(&mut self, dir: Vec2, speed: f32) {
        self.speed += dir * speed;
    }

    fn mutate(&mut self) {
        let r = gen_range(0, self.genome.len());
        self.genome.remove(r);
        self.genome.insert(r, random_gene());
        self.set_from_genome();
    }

    fn base_life(&self) -> f32 {
        8. * self.weight()
    }

    fn metabolism(&self) -> f32 {
        0.2 * (4.5 * self.attack + 2.3 * self.defense + 2.5 * self.motion + 0.1 * self.intelligence)
    }

    fn weight(&self) -> f32 {
        self.attack + self.defense + self.photosynthesis + self.motion
    }

    pub fn draw(&self) {
        let power = self.attack + self.defense + self.motion;
        let x = self.pos.x;
        let y = self.pos.y;
        let scale = 9.;
        if self.intelligence > 0. {
            draw_circle(x, y, scale * (0.2 + self.photosynthesis + power), WHITE);
        }
        draw_circle(x, y, scale * (self.photosynthesis + power), GREEN);
        draw_circle(x, y, scale * (power), RED);
        draw_circle(x, y, scale * (power - self.attack), DARKBLUE);
        draw_circle(x, y, scale * (power - self.attack - self.defense), BLUE);
    }
}


pub struct TreePoint {
    pub x: f32,
    pub y: f32,
    pub idx: usize,
}

impl RTreeObject for TreePoint {
    type Envelope = AABB<[f64; 2]>;
    fn envelope(&self) -> Self::Envelope {
        AABB::from_point([self.x as f64, self.y as f64])
    }
}

impl PointDistance for TreePoint {
    fn distance_2(
        &self,
        point: &<<Self as rstar::RTreeObject>::Envelope as rstar::Envelope>::Point,
    ) -> <<<Self as rstar::RTreeObject>::Envelope as rstar::Envelope>::Point as rstar::Point>::Scalar
    {
        (self.x as f64 - point[0]).powf(2.) + (self.y as f64 - point[1]).powf(2.)
    }
}

fn modulus<T>(a: T, b: T) -> T
where
    T: std::ops::Rem<Output = T> + std::ops::Add<Output = T> + Copy,
{
    ((a % b) + b) % b
}
