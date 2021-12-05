use macroquad::prelude::*;
use std::f32::consts::PI;

const Y_AXIS: (f32, f32, f32) = (0., 1., 0.);
const Z_AXIS: (f32, f32, f32) = (0., 0., 1.);

trait Camera {
    fn draw(&mut self);
}

struct OrbitCamera {
    position: Vec3,
    up: Vec3,
    target: Vec3,
    rot: Vec2,
    mouse: Vec2,
}

impl Camera for OrbitCamera {
    fn draw(&mut self) {
        let key_rot = |key, v| {
            if is_key_down(key) {
                v / 30.
            } else {
                vec2(0., 0.)
            }
        };

        self.rot += key_rot(KeyCode::W, vec2(0., 1.));
        self.rot += key_rot(KeyCode::A, vec2(1., 0.));
        self.rot += key_rot(KeyCode::S, vec2(0., -1.));
        self.rot += key_rot(KeyCode::D, vec2(-1., 0.));

        let new_mouse: Vec2 = mouse_position().into();
        if is_mouse_button_down(MouseButton::Left) {
            self.rot += (new_mouse - self.mouse) / 100.;
        }
        self.mouse = new_mouse;

        self.rot[0] %= 2. * PI;
        self.rot[1] = self.rot[1].max(0.2).min(PI / 2.);

        let p = Quat::from_axis_angle(Vec3::from(Y_AXIS), -self.rot[0]);
        let q = Quat::from_axis_angle(Vec3::from(Z_AXIS), -self.rot[1]);
        let rotation = p * q;

        let position = rotation.mul_vec3(self.position);
        let up = rotation.mul_vec3(self.up);
        let target = self.target;

        set_camera(&Camera3D {
            position,
            up,
            target,
            ..Default::default()
        });
    }
}

pub async fn run() {
    let rust_logo = load_texture("assets/rust.png").await.unwrap();
    let ferris = load_texture("assets/ferris.png").await.unwrap();

    let mut camera = OrbitCamera {
        position: vec3(-20., 0., 0.),
        up: vec3(0., 1., 0.),
        target: vec3(0., 0., 0.),
        rot: vec2(0., 0.2),
        mouse: mouse_position().into(),
    };

    loop {
        clear_background(LIGHTGRAY);

        camera.draw();

        draw_grid(20, 1., BLACK, GRAY);

        draw_plane(vec3(-8., 0., -8.), vec2(5., 5.), ferris, WHITE);

        draw_cube_wires(vec3(0., 1., -6.), vec3(2., 2., 2.), DARKGREEN);
        draw_cube_wires(vec3(0., 1., 6.), vec3(2., 2., 2.), DARKBLUE);
        draw_cube_wires(vec3(2., 1., 2.), vec3(2., 2., 2.), YELLOW);

        draw_cube(vec3(-5., 1., -2.), vec3(2., 2., 2.), rust_logo, WHITE);
        draw_cube(vec3(-5., 1., 2.), vec3(2., 2., 2.), ferris, WHITE);
        draw_cube(vec3(2., 0., -2.), vec3(0.4, 0.4, 0.4), None, BLACK);

        draw_sphere(vec3(-8., 0., 0.), 1., None, BLUE);

        set_default_camera();

        draw_text(
            format!("Hello World {}", get_fps()).as_str(),
            10.0,
            20.0,
            30.0,
            BLACK,
        );

        next_frame().await
    }
}
