use array2d::Array2D;
use macroquad::prelude::*;

pub struct World2D<T> {
    pub width: usize,
    pub height: usize,
    pub color_cell: fn(&T) -> Color,
    pub camera: Camera2D,
    pub bg_color: Color,
    pub pixel_size: f32,
    pub pixel_gap: f32,
    pub screen_width: f32,
    pub screen_height: f32,
}

impl<T> Default for World2D<T> {
    fn default() -> Self {
        Self {
            width: screen_width() as usize,
            height: screen_height() as usize,
            color_cell: |_| WHITE,
            screen_width: screen_width(),
            screen_height: screen_height(),
            camera: Camera2D {
                zoom: vec2(1., 1.),
                target: vec2(screen_width() / 2., screen_height() / 2.),
                ..Default::default()
            },
            bg_color: BLACK,
            pixel_size: 1.,
            pixel_gap: 0.,
        }
    }
}

impl<T> World2D<T> {
    pub fn from_world(
        width: usize,
        height: usize,
        color_cell: fn(&T) -> Color,
        bg_color: Color,
    ) -> World2D<T> {
        World2D {
            width,
            height,
            color_cell,
            bg_color,
            camera: Camera2D {
                zoom: vec2(1. / 200., 1. / 200.),
                target: vec2(5. * (width / 2) as f32, 5. * (height / 2) as f32),
                ..Default::default()
            },
            pixel_size: 5.,
            pixel_gap: 0.2,
            ..Default::default()
        }
    }

    fn draw_pre(&mut self) {
        clear_background(self.bg_color);

        set_camera(&self.camera);

        self.screen_width = screen_width();
        self.screen_height = screen_height();

        if is_key_down(KeyCode::E) {
            self.camera.zoom *= 1.1;
        }
        if is_key_down(KeyCode::Q) {
            self.camera.zoom /= 1.1;
        }
        let mut key_rot = |key: KeyCode, v: (f32, f32)| {
            if is_key_down(key) {
                self.camera.target = vec2(
                    self.camera.target[0] + v.0 * 0.05 / self.camera.zoom[0],
                    self.camera.target[1] + v.1 * 0.06 / self.camera.zoom[1],
                );
            }
        };
        key_rot(KeyCode::W, (0., 1.));
        key_rot(KeyCode::A, (-1., 0.));
        key_rot(KeyCode::S, (0., -1.));
        key_rot(KeyCode::D, (1., 0.));
    }

    pub async fn draw_post(&mut self) {
        set_default_camera();
        next_frame().await
    }

    pub async fn draw(&mut self, world: &[T], frames: usize) {
        for _ in 0..frames {
            if is_key_down(KeyCode::LeftSuper) && is_key_down(KeyCode::Q) {
                return;
            }
            self.draw_pre();
            for (i, c) in world.iter().enumerate() {
                let color = (self.color_cell)(c);
                if color == self.bg_color {
                    continue;
                }

                draw_rectangle(
                    self.pixel_size * (i / self.width) as f32,
                    self.pixel_size * (i % self.width) as f32,
                    self.pixel_size - self.pixel_gap,
                    self.pixel_size - self.pixel_gap,
                    color,
                );
            }
            self.draw_post().await;
        }
    }
}

impl<T: Clone> World2D<T> {
    pub fn from_grid(
        grid: &Array2D<T>,
        color_cell: fn(&T) -> Color,
        bg_color: Color,
    ) -> World2D<T> {
        World2D {
            width: grid.row_len(),
            height: grid.column_len(),
            color_cell,
            bg_color,
            camera: Camera2D {
                zoom: vec2(1. / 200., 1. / 200.),
                target: vec2(
                    5. * (grid.row_len() / 2) as f32,
                    5. * (grid.column_len() / 2) as f32,
                ),
                ..Default::default()
            },
            pixel_size: 5.,
            pixel_gap: 0.2,
            ..Default::default()
        }
    }

    pub async fn draw_grid(&mut self, world: &Array2D<T>, frames: usize) {
        for _ in 0..frames {
            if is_key_down(KeyCode::LeftSuper) && is_key_down(KeyCode::Q) {
                return;
            }
            self.draw_pre();
            for (i, p) in world.elements_row_major_iter().enumerate() {
                let color = (self.color_cell)(p);
                if color == self.bg_color {
                    continue;
                }
                draw_rectangle(
                    self.pixel_size * (i / self.width) as f32,
                    self.pixel_size * (i % self.width) as f32,
                    self.pixel_size - self.pixel_gap,
                    self.pixel_size - self.pixel_gap,
                    color,
                );
            }

            self.draw_post().await;
        }
    }
}

impl World2D<(i32, i32)> {
    pub async fn draw_pixels(&mut self, world: &[(i32, i32)], frames: usize) {
        for _ in 0..frames {
            if is_key_down(KeyCode::LeftSuper) && is_key_down(KeyCode::Q) {
                return;
            }
            self.draw_pre();
            for p in world.iter() {
                let color = (self.color_cell)(p);
                if color == self.bg_color {
                    continue;
                }
                draw_rectangle(
                    p.0 as f32 * self.pixel_size,
                    -p.1 as f32 * self.pixel_size,
                    self.pixel_size - self.pixel_gap,
                    self.pixel_size - self.pixel_gap,
                    color,
                );
            }
            self.draw_post().await;
        }
    }
}
