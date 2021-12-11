use macroquad::prelude::*;

pub struct World2D<T> {
    width: usize,
    height: usize,
    color_cell: fn(&T) -> Color,
    screen_width: f32,
    screen_height: f32,
    camera: Camera2D,
    bg_color: Color,
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
            screen_width: screen_width(),
            screen_height: screen_height(),
            camera: Camera2D {
                zoom: vec2(1. / 200., 1. / 200.),
                target: vec2(20. * (width / 2) as f32, 20. * (height / 2) as f32),
                ..Default::default()
            },
        }
    }

    pub fn draw(&mut self, world: &[T]) {
        clear_background(self.bg_color);

        set_camera(&self.camera);

        // let needs_update =
        //     screen_width() != self.screen_width || screen_height() != self.screen_height || update;

        // self.image = image;
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

        for (i, c) in world.iter().enumerate() {
            let color = (self.color_cell)(c);
            if color == self.bg_color {
                continue;
            }

            draw_rectangle(
                20. * (i / self.width) as f32,
                20. * (i % self.width) as f32,
                19.,
                19.,
                color,
            );
        }

        set_default_camera();
    }
}

pub async fn run() {}
