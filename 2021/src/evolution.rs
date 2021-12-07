use macroquad::prelude::*;
use rand::gen_range;
use rayon::prelude::*;
use rstar::{PointDistance, RTree, RTreeObject, AABB};
use std::{
    thread,
    time::{Duration, Instant},
};

const LETTERS: &[char] = &['a', 'd', 'p', 'm', 'n', 'n', 'n', 'i'];

fn random_gene() -> char {
    LETTERS[gen_range(0, LETTERS.len() as u32) as usize]
}

pub async fn run() {
    rand::srand(miniquad::date::now().to_bits());
    let mut biots = BiotCollection::new(500, vec2(screen_width(), screen_height()));

    let _pool = rayon::ThreadPoolBuilder::new()
        .num_threads(16)
        .build()
        .unwrap();

    let mut now = Instant::now();
    loop {
        biots.step(vec2(screen_width(), screen_height()));
        clear_background(Color::new(0., 0., 0.1, 1.0));
        biots.draw();
        draw_text(
            &format!("FPS: {}, biots: {}", get_fps(), biots.size()),
            screen_width() - 250.,
            screen_height() - 5.,
            28.,
            LIGHTGRAY,
        );
        let ft = now.elapsed();
        if ft.as_nanos() < 32000000 {
            thread::sleep(Duration::from_nanos(32000000 - ft.as_nanos() as u64));
        }
        now = Instant::now();
        next_frame().await
    }
}

#[derive(Clone, Debug)]
pub struct BiotCollection {
    biots: Vec<Biot>,
}

impl BiotCollection {
    pub fn new(n: usize, screen: Vec2) -> Self {
        Self {
            biots: (0..n).map(|_i| Biot::random_new(screen)).collect(),
        }
    }

    pub fn draw(&self) {
        self.biots.iter().for_each(|b| b.draw())
    }

    pub fn size(&self) -> usize {
        self.biots.len()
    }

    pub fn step(&mut self, screen: Vec2) {
        let tree = RTree::bulk_load(
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

        let dirs = self.find_prey(&tree);

        let mut new = self
            .biots
            .par_iter_mut()
            .enumerate()
            .map(|(n, biot)| biot.step(&tree, dirs[n], screen))
            .flatten()
            .collect();

        let lifes = self.interact(&tree);

        for i in 0..lifes.len() {
            let l = lifes[i];
            let c = self.biots[i].life;
            self.biots[i].life = match l {
                None => 0.,
                Some(e) => c + e,
            }
        }
        self.biots.retain(|b| !b.dead());
        self.biots.append(&mut new);
    }

    fn find_prey(&mut self, tree: &RTree<TreePoint>) -> Vec<Option<Vec2>> {
        (0..self.biots.len())
            .into_par_iter()
            .map(|n| match self.biots[n].intelligence {
                i if i == 0. => None,
                _ => tree
                    .nearest_neighbor_iter_with_distance_2(&[
                        self.biots[n].pos.x as f64,
                        self.biots[n].pos.y as f64,
                    ])
                    .take_while(|(_other, d2)| {
                        *d2 as f32 > (self.biots[n].intelligence.powf(2.)) * 1600.
                    })
                    .find(|(other, _d2)| {
                        other.idx != n && self.biots[n].stronger(&self.biots[other.idx])
                    })
                    .map(|(other, _d2)| {
                        vec2(
                            other.x as f32 - self.biots[n].pos.x,
                            other.y as f32 - self.biots[n].pos.y,
                        )
                        .normalize()
                    }),
            })
            .collect::<Vec<Option<Vec2>>>()
    }

    fn interact(&mut self, tree: &RTree<TreePoint>) -> Vec<Option<f32>> {
        (0..self.biots.len())
            .into_par_iter()
            .map(|n| {
                let mut life = Some(0.);
                for s in tree.locate_within_distance(
                    [self.biots[n].pos.x as f64, self.biots[n].pos.y as f64],
                    100.,
                ) {
                    if s.idx != n {
                        let i = n;
                        let j = s.idx;
                        let dist = (self.biots[i].pos - self.biots[j].pos).length();
                        if dist < 20. * (self.biots[i].weight() + self.biots[j].weight()) {
                            if self.biots[i].stronger(&self.biots[j]) {
                                life = life.map(|l| l + self.biots[j].life * 0.8);
                            } else if self.biots[j].stronger(&self.biots[i]) {
                                return None;
                            }
                        }
                    }
                }
                life
            })
            .collect::<Vec<Option<f32>>>()
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
    pub feed_dir: Option<Vec2>,
}

// struct Parameters {
//     adult_factor: f32,
//     reproduction_area: f32,
//     reproduction_mutation: f32,
//     reproduction_speed: f32,
//     reproduction_life: f32,
//     speed_decay: f32,
//     photo_life: f32,
//     motion_chance: f32,
//     speed_scale: f32,
//     max_age: f32,
//     defense_scale: f32,
//     base_life_scale: f32,
//     metabolism_global: f32,
//     metabolism_attack: f32,
//     metabolism_defense: f32,
//     metabolism_motion: f32,
//     metabolism_intelligence: f32,
//     location_distance: f32,
//     interaction_distance: f32,
// }

impl Biot {
    pub fn random_new(screen: Vec2) -> Self {
        let genome = (0..13).map(|_i| random_gene()).collect();
        let mut s = Self {
            life: 0.,
            pos: vec2(gen_range(0., 1.) * screen[0], gen_range(0., 1.) * screen[1]),
            speed: vec2(0., 0.),
            age: 0,
            genome,
            attack: 0.,
            defense: 0.,
            photosynthesis: 0.,
            motion: 0.,
            intelligence: 0.,
            feed_dir: None,
        };
        s.set_from_genome();
        s.life = s.base_life();
        s
    }

    pub fn step(
        &mut self,
        rtree: &RTree<TreePoint>,
        feed_dir: Option<Vec2>,
        screen: Vec2,
    ) -> Option<Biot> {
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
        self.pos.x = modulus(self.pos.x, screen[0]);
        self.pos.y = modulus(self.pos.y, screen[1]);
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

    pub fn dead(&self) -> bool {
        self.life <= 0. || self.age >= 10000
    }

    pub fn stronger(&self, other: &Self) -> bool {
        self.attack > other.attack + other.defense * 0.5
    }

    fn set_from_genome(&mut self) {
        let cnt = |l| self.genome.iter().filter(|&&c| c == l).count() as f32;
        self.attack = cnt('a') * 0.1;
        self.defense = cnt('d') * 0.1;
        self.photosynthesis = cnt('p') * 0.1;
        self.motion = cnt('m') * 0.1;
        self.intelligence = cnt('i') * 10.;
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
        0.2 * (3.5 * self.attack + 2.3 * self.defense + 2.5 * self.motion + 0.1 * self.intelligence)
    }

    fn weight(&self) -> f32 {
        self.attack + self.defense + self.photosynthesis + self.motion
    }

    pub fn draw(&self) {
        let x = self.pos.x;
        let y = self.pos.y;
        let scale = 9.;
        let mut weight = self.weight();
        if self.intelligence > 0. {
            draw_circle(x, y, scale * (0.2 + weight), WHITE);
        }
        draw_circle(x, y, scale * weight, GREEN);
        weight -= self.photosynthesis;
        draw_circle(x, y, scale * weight, RED);
        weight -= self.attack;
        draw_circle(x, y, scale * weight, DARKBLUE);
        weight -= self.defense;
        draw_circle(x, y, scale * weight, BLUE);
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

extern crate test;

#[cfg(test)]
mod tests {
    use super::test::black_box;
    use super::test::Bencher;
    use super::BiotCollection;
    use macroquad::prelude::*;

    #[bench]
    fn bench_biots_step(b: &mut Bencher) {
        let _pool = rayon::ThreadPoolBuilder::new()
            .num_threads(16)
            .build()
            .unwrap();
        rand::srand(0);
        let mut biots = BiotCollection::new(10000, vec2(800., 600.));
        b.iter(|| {
            black_box(biots.step(vec2(800., 600.)));
        });
    }
}
