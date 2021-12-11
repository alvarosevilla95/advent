use macroquad::prelude::*;

pub struct World2d<'a> {
    pub image: &'a Image,
    texture: Texture2D,
    screen_width: f32,
    screen_height: f32,
}

impl World2d<'_> {
    pub fn new(image: &Image) -> World2d {
        World2d {
            image,
            texture: Texture2D::from_image(image),
            screen_width: 0.,
            screen_height: 0.,
        }
    }

    pub async fn draw(&mut self, update: bool) {
        clear_background(Color::new(0., 0., 0.1, 1.0));

        let needs_update =
            screen_width() != self.screen_width || screen_height() != self.screen_height || update;

        // self.image = image;
        self.screen_width = screen_width();
        self.screen_height = screen_height();

        let aspect_ratio = self.image.width() as f32 / self.image.height() as f32;
        let screen_aspect_ratio = screen_width() / screen_height();
        let ratio = screen_aspect_ratio - aspect_ratio;
        let x_off = if ratio > 0. {
            screen_width() * (ratio / screen_aspect_ratio)
        } else {
            0.
        };
        let y_off = if ratio < 0. {
            -screen_height() * ratio
        } else {
            0.
        };
        if needs_update {
            info!("updating");
            self.texture = Texture2D::from_image(self.image);
        }
        draw_texture_ex(
            self.texture,
            x_off / 2.,
            y_off / 2.,
            WHITE,
            DrawTextureParams {
                dest_size: Some(vec2(screen_width() - x_off, screen_height() - y_off)),
                ..Default::default()
            },
        );
        draw_text(format!("{}", get_fps()).as_str(), 10.0, 20.0, 30.0, WHITE);
    }
}

pub async fn run() {}
