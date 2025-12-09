# claude made this and it's great

import pygame
import sys
import math
import random
from collections import deque

# Parse data
data = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
""".strip()

data = open('inputs/day9.txt').read()

points = list(map(eval, data.splitlines()))
segments = [(points[i], points[(i+1) % len(points)]) for i in range(len(points))]

def point_inside(cx, cy):
    crossings = 0
    for (x1, y1), (x2, y2) in segments:
        if x1 == x2 and x1 > cx and min(y1, y2) <= cy < max(y1, y2):
            crossings += 1
    return crossings % 2 == 1

def area(a, b):
    return (abs(a[0]-b[0])+1) * (abs(a[1]-b[1])+1)

# Coordinate compression
xs = sorted({p[0] for p in points})
ys = sorted({p[1] for p in points})
nx, ny = len(xs) - 1, len(ys) - 1

psum = [[0] * (ny+1) for _ in range(nx+1)]
inside_cells = set()
for i in range(nx):
    for j in range(ny):
        cx, cy = (xs[i] + xs[i+1]) / 2, (ys[j] + ys[j+1]) / 2
        if point_inside(cx, cy):
            inside_cells.add((i, j))
            psum[i+1][j+1] = 1 + psum[i][j+1] + psum[i+1][j] - psum[i][j]
        else:
            psum[i+1][j+1] = psum[i][j+1] + psum[i+1][j] - psum[i][j]

x_idx = {x: i for i, x in enumerate(xs)}
y_idx = {y: j for j, y in enumerate(ys)}

def rect_inside(x1, x2, y1, y2):
    i1, i2 = x_idx[x1], x_idx[x2]
    j1, j2 = y_idx[y1], y_idx[y2]
    total = psum[i2][j2] - psum[i1][j2] - psum[i2][j1] + psum[i1][j1]
    return total == (i2 - i1) * (j2 - j1)

# Pre-compute all rectangle pairs
all_pairs = [(a, b) for i, a in enumerate(points) for b in points[i+1:]]
# Sort ascending so we see the "best" update as we find bigger valid rectangles
random.shuffle(all_pairs)  # Randomize for more interesting animation

# Pre-compute answer
final_best = None
final_best_area = 0
final_valid_count = 0
for a, b in all_pairs:
    x1, x2 = min(a[0], b[0]), max(a[0], b[0])
    y1, y2 = min(a[1], b[1]), max(a[1], b[1])
    if rect_inside(x1, x2, y1, y2):
        final_valid_count += 1
        if area(a, b) > final_best_area:
            final_best_area = area(a, b)
            final_best = (a, b)

# Pygame setup
pygame.init()
# Fullscreen mode - set mode first, then get actual dimensions
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
MARGIN = 50  # Smaller margins to use more screen
pygame.display.set_caption("Day 9 - Red & Green Tiles")
clock = pygame.time.Clock()

# Cyberpunk color palette
BG_COLOR = (10, 12, 18)
GRID_COLOR = (25, 30, 45)
GRID_GLOW = (40, 50, 80)
GREEN_DARK = (20, 80, 40)
GREEN_MID = (40, 160, 80)
GREEN_BRIGHT = (80, 255, 120)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 128)
RED_COLOR = (255, 60, 80)
GOLD = (255, 200, 50)
GOLD_BRIGHT = (255, 230, 100)
TEXT_COLOR = (200, 210, 230)
TEXT_DIM = (100, 110, 130)

# Scale fonts based on screen size
font_scale = min(WIDTH / 1200, HEIGHT / 900)
font_small = pygame.font.Font(None, int(22 * font_scale))
font_med = pygame.font.Font(None, int(32 * font_scale))
font_large = pygame.font.Font(None, int(48 * font_scale))
font_huge = pygame.font.Font(None, int(80 * font_scale))
font_massive = pygame.font.Font(None, int(120 * font_scale))

# Animation state
class State:
    INTRO = 0
    DRAW_POLYGON = 1
    FILL_CELLS = 2
    CHECK_RECTS = 3
    SHOW_RESULT = 4

state = State.INTRO
animation_time = 0
global_time = 0
filled_cells = []
current_pair_idx = 0
best_valid = None
best_area = 0
checked_count = 0
valid_count = 0
particles = []
skip_animation = False
speed_multiplier = 1.0
screen_shake = 0
scan_line_y = 0
flash_alpha = 0
new_best_flash = 0
last_checked_rect = None
checking_history = deque(maxlen=8)  # Trail of recent checks

# Enhanced Particle class
class Particle:
    def __init__(self, x, y, color, style='spark'):
        self.x, self.y = x, y
        self.style = style
        if style == 'spark':
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 8)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
            self.size = random.uniform(2, 5)
            self.life = 1.0
            self.decay = random.uniform(1.5, 2.5)
        elif style == 'star':
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(-3, -1)
            self.size = random.uniform(3, 8)
            self.life = 1.0
            self.decay = random.uniform(0.8, 1.2)
            self.rotation = random.uniform(0, math.pi * 2)
            self.rot_speed = random.uniform(-5, 5)
        elif style == 'ring':
            self.size = 5
            self.max_size = random.uniform(30, 60)
            self.life = 1.0
            self.decay = 2.0
            self.vx = self.vy = 0
        self.color = color

    def update(self, dt):
        self.life -= dt * self.decay
        if self.style == 'spark':
            self.x += self.vx
            self.y += self.vy
            self.vy += 0.3
            self.vx *= 0.98
        elif self.style == 'star':
            self.x += self.vx
            self.y += self.vy
            self.rotation += self.rot_speed * dt
        elif self.style == 'ring':
            self.size += (self.max_size - self.size) * 0.1
        return self.life > 0

    def draw(self, surface):
        alpha = int(max(0, min(255, self.life * 255)))
        if self.style == 'spark':
            color = (*self.color[:3], alpha)
            size = max(1, self.size * self.life)
            s = pygame.Surface((size*2+4, size*2+4), pygame.SRCALPHA)
            # Glow
            pygame.draw.circle(s, (*self.color[:3], alpha//3), (size+2, size+2), size+2)
            pygame.draw.circle(s, color, (size+2, size+2), size)
            surface.blit(s, (self.x - size - 2, self.y - size - 2))
        elif self.style == 'star':
            self._draw_star(surface, alpha)
        elif self.style == 'ring':
            color = (*self.color[:3], alpha//2)
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), int(self.size), 2)

    def _draw_star(self, surface, alpha):
        points = []
        for i in range(5):
            angle = self.rotation + i * math.pi * 2 / 5 - math.pi / 2
            r = self.size if i % 2 == 0 else self.size * 0.4
            points.append((self.x + math.cos(angle) * r, self.y + math.sin(angle) * r))
            angle += math.pi / 5
            r = self.size * 0.4 if i % 2 == 0 else self.size
            points.append((self.x + math.cos(angle) * r, self.y + math.sin(angle) * r))
        s = pygame.Surface((self.size*3, self.size*3), pygame.SRCALPHA)
        offset_points = [(p[0] - self.x + self.size*1.5, p[1] - self.y + self.size*1.5) for p in points]
        pygame.draw.polygon(s, (*self.color[:3], alpha), offset_points)
        surface.blit(s, (self.x - self.size*1.5, self.y - self.size*1.5))


def ease_out_elastic(t):
    if t == 0 or t == 1:
        return t
    p = 0.3
    return math.pow(2, -10 * t) * math.sin((t - p/4) * (2 * math.pi) / p) + 1

def ease_out_back(t):
    c1, c3 = 1.70158, c1 + 1
    return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)

def ease_in_out_cubic(t):
    return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def compressed_to_screen(i, j):
    sx = MARGIN + i * (WIDTH - 2*MARGIN) / max(len(xs), 1)
    sy = MARGIN + (len(ys) - 1 - j) * (HEIGHT - 2*MARGIN) / max(len(ys), 1)
    return sx, sy

def get_rect_screen(a, b):
    x1, x2 = min(a[0], b[0]), max(a[0], b[0])
    y1, y2 = min(a[1], b[1]), max(a[1], b[1])
    i1, i2 = x_idx[x1], x_idx[x2]
    j1, j2 = y_idx[y1], y_idx[y2]
    sx1, sy1 = compressed_to_screen(i1, j2)
    sx2, sy2 = compressed_to_screen(i2, j1)
    return sx1, sy1, sx2 - sx1, sy2 - sy1

def draw_background():
    screen.fill(BG_COLOR)
    # Animated grid
    offset = (global_time * 20) % 40
    for i in range(0, WIDTH + 40, 40):
        alpha = 20 + 10 * math.sin(global_time * 2 + i * 0.1)
        pygame.draw.line(screen, (*GRID_COLOR[:3],), (i - offset, 0), (i - offset, HEIGHT))
    for j in range(0, HEIGHT + 40, 40):
        pygame.draw.line(screen, GRID_COLOR, (0, j - offset), (WIDTH, j - offset))

def draw_grid():
    # Subtle glow on grid lines
    for i in range(len(xs)):
        sx, _ = compressed_to_screen(i, 0)
        glow = 30 + 15 * math.sin(global_time * 3 + i * 0.5)
        pygame.draw.line(screen, (30, int(40 + glow), 60), (sx, MARGIN-10), (sx, HEIGHT - MARGIN+10), 1)
    for j in range(len(ys)):
        _, sy = compressed_to_screen(0, j)
        glow = 30 + 15 * math.sin(global_time * 3 + j * 0.5)
        pygame.draw.line(screen, (30, int(40 + glow), 60), (MARGIN-10, sy), (WIDTH - MARGIN+10, sy), 1)

def draw_filled_cells(cells, pulse=False):
    for i, j in cells:
        sx1, sy1 = compressed_to_screen(i, j+1)
        sx2, sy2 = compressed_to_screen(i+1, j)
        w, h = sx2 - sx1, sy2 - sy1
        # Gradient effect
        brightness = 0.7 + 0.3 * math.sin(global_time * 2 + i * 0.3 + j * 0.3) if pulse else 1.0
        color = lerp_color(GREEN_DARK, GREEN_MID, brightness)
        pygame.draw.rect(screen, color, (sx1+1, sy1+1, w-2, h-2))
        # Edge glow
        pygame.draw.rect(screen, GREEN_MID, (sx1, sy1, w, h), 1)

def draw_polygon_fancy(segment_count, progress=1.0):
    if segment_count == 0:
        return

    all_points = []
    for idx in range(min(segment_count + 1, len(points))):
        p = points[idx % len(points)]
        all_points.append(compressed_to_screen(x_idx[p[0]], y_idx[p[1]]))

    if len(all_points) < 2:
        return

    # Draw glow first
    for idx in range(len(all_points) - 1):
        start, end = all_points[idx], all_points[idx + 1]
        for glow in range(3, 0, -1):
            alpha = 30 // glow
            pygame.draw.line(screen, (*GREEN_BRIGHT[:3],), start, end, glow * 2 + 1)

    # Draw main lines
    for idx in range(len(all_points) - 1):
        start, end = all_points[idx], all_points[idx + 1]
        # Animated dash effect
        length = math.sqrt((end[0]-start[0])**2 + (end[1]-start[1])**2)
        if length > 0:
            dx, dy = (end[0]-start[0])/length, (end[1]-start[1])/length
            dash_offset = (global_time * 50) % 20
            for d in range(0, int(length), 10):
                d_start = d + dash_offset
                d_end = min(d_start + 6, length)
                if d_start < length:
                    p1 = (start[0] + dx * d_start, start[1] + dy * d_start)
                    p2 = (start[0] + dx * d_end, start[1] + dy * d_end)
                    pygame.draw.line(screen, GREEN_BRIGHT, p1, p2, 3)

def draw_points_fancy(count=None, pulse=False, highlight_idx=None):
    if count is None:
        count = len(points)
    for idx, p in enumerate(points[:count]):
        sx, sy = compressed_to_screen(x_idx[p[0]], y_idx[p[1]])

        # Outer glow
        for r in range(20, 5, -3):
            alpha = 30 - r
            s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*RED_COLOR[:3], alpha), (r, r), r)
            screen.blit(s, (sx - r, sy - r))

        radius = 8
        if pulse:
            radius += math.sin(global_time * 5 + idx) * 2

        # Main circle
        pygame.draw.circle(screen, RED_COLOR, (int(sx), int(sy)), int(radius))
        pygame.draw.circle(screen, (255, 150, 150), (int(sx), int(sy)), int(radius - 2))
        pygame.draw.circle(screen, (255, 255, 255), (int(sx), int(sy)), int(radius), 2)

def draw_rect_checking(a, b, progress, is_valid=None):
    sx, sy, w, h = get_rect_screen(a, b)

    # Scanning effect
    scan_h = int(h * progress)

    # Draw scan line
    if progress < 1.0:
        scan_y = sy + scan_h
        pygame.draw.line(screen, CYAN, (sx, scan_y), (sx + w, scan_y), 2)
        # Glow on scan line
        for g in range(1, 4):
            pygame.draw.line(screen, (*CYAN[:3],), (sx, scan_y - g), (sx + w, scan_y - g), 1)
            pygame.draw.line(screen, (*CYAN[:3],), (sx, scan_y + g), (sx + w, scan_y + g), 1)

    # Scanning fill
    s = pygame.Surface((w, scan_h), pygame.SRCALPHA)
    s.fill((*CYAN[:3], 40))
    screen.blit(s, (sx, sy))

    # Border
    color = CYAN if is_valid is None else (GREEN_BRIGHT if is_valid else MAGENTA)
    pygame.draw.rect(screen, color, (sx, sy, w, h), 2)

    # Corner markers
    corner_size = min(15, w//4, h//4)
    for cx, cy in [(sx, sy), (sx+w, sy), (sx, sy+h), (sx+w, sy+h)]:
        dx = corner_size if cx == sx else -corner_size
        dy = corner_size if cy == sy else -corner_size
        pygame.draw.line(screen, color, (cx, cy), (cx + dx, cy), 2)
        pygame.draw.line(screen, color, (cx, cy), (cx, cy + dy), 2)

def draw_best_rect(a, b):
    sx, sy, w, h = get_rect_screen(a, b)

    pulse = 0.7 + 0.3 * math.sin(global_time * 4)

    # Animated glow layers
    for i in range(5, 0, -1):
        expand = i * 6 * pulse
        alpha = int(40 * pulse / i)
        s = pygame.Surface((w + expand*2, h + expand*2), pygame.SRCALPHA)
        pygame.draw.rect(s, (*GOLD[:3], alpha), (0, 0, w + expand*2, h + expand*2), border_radius=3)
        screen.blit(s, (sx - expand, sy - expand))

    # Main fill
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    s.fill((*GOLD[:3], int(80 * pulse)))
    screen.blit(s, (sx, sy))

    # Animated border
    pygame.draw.rect(screen, GOLD_BRIGHT, (sx, sy, w, h), 3)

    # Sparkle corners
    for cx, cy in [(sx, sy), (sx+w, sy), (sx, sy+h), (sx+w, sy+h)]:
        sparkle = 5 + 3 * math.sin(global_time * 8 + cx + cy)
        pygame.draw.circle(screen, GOLD_BRIGHT, (int(cx), int(cy)), int(sparkle))

def draw_checking_history():
    for idx, (a, b, is_valid, age) in enumerate(checking_history):
        alpha = max(0, 1 - age) * 0.5
        if alpha <= 0:
            continue
        sx, sy, w, h = get_rect_screen(a, b)
        color = GREEN_MID if is_valid else MAGENTA
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        s.fill((*color[:3], int(alpha * 60)))
        screen.blit(s, (sx, sy))
        pygame.draw.rect(screen, (*color[:3],), (sx, sy, w, h), 1)

def spawn_particles(x, y, count=20, color=GOLD, style='spark'):
    for _ in range(count):
        particles.append(Particle(x, y, color, style))

def spawn_celebration(x, y, w, h):
    # Spawn various particle types
    for _ in range(30):
        spawn_particles(x + random.uniform(0, w), y + random.uniform(0, h), 1, GOLD, 'spark')
    for _ in range(10):
        spawn_particles(x + random.uniform(0, w), y + random.uniform(0, h), 1, GOLD_BRIGHT, 'star')
    for _ in range(3):
        spawn_particles(x + w/2, y + h/2, 1, GOLD, 'ring')

def draw_progress_bar():
    bar_w, bar_h = min(250, WIDTH // 5), 25
    bar_x, bar_y = WIDTH - bar_w - 100, 25

    # Background
    pygame.draw.rect(screen, (30, 35, 50), (bar_x-2, bar_y-2, bar_w+4, bar_h+4), border_radius=5)
    pygame.draw.rect(screen, (20, 25, 35), (bar_x, bar_y, bar_w, bar_h), border_radius=3)

    # Progress fill with gradient effect
    progress = checked_count / max(len(all_pairs), 1)
    fill_w = int(bar_w * progress)
    if fill_w > 0:
        for i in range(fill_w):
            t = i / bar_w
            color = lerp_color((200, 150, 0), GOLD_BRIGHT, t)
            pygame.draw.line(screen, color, (bar_x + i, bar_y + 2), (bar_x + i, bar_y + bar_h - 2))

    # Animated shine
    shine_x = (global_time * 100) % (bar_w + 50) - 25
    if 0 < shine_x < fill_w:
        for i in range(-10, 10):
            alpha = max(0, 100 - abs(i) * 10)
            pygame.draw.line(screen, (255, 255, 255, alpha),
                           (bar_x + shine_x + i, bar_y), (bar_x + shine_x + i, bar_y + bar_h))

    # Border
    pygame.draw.rect(screen, GOLD, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=3)

    # Percentage text
    pct_text = font_med.render(f"{progress*100:.0f}%", True, TEXT_COLOR)
    screen.blit(pct_text, (bar_x + bar_w + 10, bar_y + 2))

def draw_info():
    # Top left info with style
    info_lines = [
        (f"POINTS: {len(points)}", TEXT_DIM),
        (f"GRID: {nx}×{ny}", TEXT_DIM),
        (f"SPEED: {speed_multiplier}x", CYAN if speed_multiplier != 1.0 else TEXT_DIM),
    ]

    for i, (text, color) in enumerate(info_lines):
        rendered = font_small.render(text, True, color)
        screen.blit(rendered, (15, 15 + i * 22))

    if state >= State.CHECK_RECTS:
        # Stats
        stats_y = 90
        checked_text = font_med.render(f"Checked: {checked_count:,}", True, TEXT_COLOR)
        screen.blit(checked_text, (15, stats_y))

        valid_text = font_med.render(f"Valid: {valid_count:,}", True, GREEN_BRIGHT)
        screen.blit(valid_text, (15, stats_y + 30))

        if best_area > 0:
            best_text = font_large.render(f"BEST: {best_area:,}", True, GOLD_BRIGHT)
            # Glow effect on text
            glow_surf = font_large.render(f"BEST: {best_area:,}", True, GOLD)
            screen.blit(glow_surf, (14, stats_y + 59))
            screen.blit(best_text, (15, stats_y + 60))

        draw_progress_bar()

def draw_title_screen():
    # Animated title
    title_text = "DAY 9"
    title_render = font_massive.render(title_text, True, GREEN_BRIGHT)
    glow_render = font_massive.render(title_text, True, (*GREEN_MID[:3],))

    title_y = HEIGHT//2 - title_render.get_height() - 20
    title_x = WIDTH//2 - title_render.get_width()//2

    screen.blit(glow_render, (title_x - 2, title_y - 2))
    screen.blit(glow_render, (title_x + 2, title_y + 2))
    screen.blit(title_render, (title_x, title_y))

    subtitle = font_large.render("Red & Green Tiles", True, TEXT_COLOR)
    subtitle_y = title_y + title_render.get_height() + 20
    screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, subtitle_y))

    # Animated instructions
    instructions = [
        ("SPACE", "Start"),
        ("S", "Skip"),
        ("+/-", "Speed"),
        ("R", "Reset"),
    ]

    inst_y = subtitle_y + subtitle.get_height() + 60
    spacing = min(120, WIDTH // 10)
    start_x = WIDTH//2 - (len(instructions) - 1) * spacing // 2

    for i, (key, action) in enumerate(instructions):
        x = start_x + i * spacing

        # Brighter colors for better contrast
        key_text = font_med.render(key, True, GOLD_BRIGHT)
        screen.blit(key_text, (x - key_text.get_width()//2, inst_y))

        action_text = font_small.render(action, True, TEXT_COLOR)
        screen.blit(action_text, (x - action_text.get_width()//2, inst_y + 35))

def draw():
    global state, animation_time, global_time, filled_cells, current_pair_idx
    global best_valid, best_area, checked_count, valid_count, skip_animation
    global screen_shake, flash_alpha, new_best_flash, last_checked_rect, checking_history

    dt = clock.get_time() / 1000.0
    animation_time += dt * speed_multiplier
    global_time += dt

    # Update screen shake
    screen_shake *= 0.9
    flash_alpha *= 0.95
    new_best_flash *= 0.92

    # Apply screen shake
    shake_offset = (random.uniform(-1, 1) * screen_shake, random.uniform(-1, 1) * screen_shake)

    draw_background()
    draw_grid()

    # Update checking history ages
    for i in range(len(checking_history)):
        a, b, v, age = checking_history[i]
        checking_history[i] = (a, b, v, age + dt * 3)

    if state == State.INTRO:
        # Preview animation
        t = (math.sin(global_time * 1.5) + 1) / 2
        preview_cells = list(inside_cells)[:int(len(inside_cells) * t)]
        draw_filled_cells(preview_cells, pulse=True)
        draw_polygon_fancy(len(segments))
        draw_points_fancy(pulse=True)
        draw_title_screen()

    elif state == State.DRAW_POLYGON:
        speed = max(15, len(segments) / 1.5)
        segment_progress = (animation_time * speed) % 1.0
        segments_to_draw = int(animation_time * speed)

        if segments_to_draw > len(segments):
            state = State.FILL_CELLS
            animation_time = 0
            filled_cells = []
        else:
            draw_polygon_fancy(segments_to_draw, segment_progress)
            draw_points_fancy(min(segments_to_draw + 1, len(points)))

            # Status text
            status = font_med.render(f"Drawing boundary... {min(segments_to_draw, len(segments))}/{len(segments)}", True, GREEN_BRIGHT)
            screen.blit(status, (WIDTH//2 - status.get_width()//2, HEIGHT - 60))

    elif state == State.FILL_CELLS:
        cells_list = list(inside_cells)
        fill_duration = 0.8
        progress = ease_in_out_cubic(min(animation_time / fill_duration, 1.0))
        target_cells = int(len(cells_list) * progress)

        if animation_time >= fill_duration:
            filled_cells = cells_list
            state = State.CHECK_RECTS
            animation_time = 0
        else:
            filled_cells = cells_list[:target_cells]

        draw_filled_cells(filled_cells, pulse=True)
        draw_polygon_fancy(len(segments))
        draw_points_fancy()

        status = font_med.render(f"Filling interior... {len(filled_cells):,}/{len(inside_cells):,}", True, GREEN_BRIGHT)
        screen.blit(status, (WIDTH//2 - status.get_width()//2, HEIGHT - 60))

    elif state == State.CHECK_RECTS:
        draw_filled_cells(inside_cells, pulse=True)
        draw_checking_history()

        if skip_animation:
            best_valid = final_best
            best_area = final_best_area
            valid_count = final_valid_count
            checked_count = len(all_pairs)
            state = State.SHOW_RESULT
            animation_time = 0
            if best_valid:
                sx, sy, w, h = get_rect_screen(best_valid[0], best_valid[1])
                spawn_celebration(sx, sy, w, h)
                screen_shake = 15
        else:
            rects_per_frame = max(1, int(len(all_pairs) // 150 * speed_multiplier))

            for _ in range(rects_per_frame):
                if current_pair_idx >= len(all_pairs):
                    state = State.SHOW_RESULT
                    animation_time = 0
                    break

                a, b = all_pairs[current_pair_idx]
                x1, x2 = min(a[0], b[0]), max(a[0], b[0])
                y1, y2 = min(a[1], b[1]), max(a[1], b[1])
                is_valid = rect_inside(x1, x2, y1, y2)
                rect_area = area(a, b)

                checked_count += 1
                last_checked_rect = (a, b, is_valid)
                checking_history.append((a, b, is_valid, 0))

                if is_valid:
                    valid_count += 1
                    if rect_area > best_area:
                        best_area = rect_area
                        best_valid = (a, b)
                        sx, sy, w, h = get_rect_screen(a, b)
                        spawn_celebration(sx, sy, w, h)
                        screen_shake = 10
                        new_best_flash = 1.0

                current_pair_idx += 1

            # Draw current check
            if last_checked_rect:
                a, b, is_valid = last_checked_rect
                draw_rect_checking(a, b, 1.0, is_valid)

            # Draw current best
            if best_valid:
                draw_best_rect(best_valid[0], best_valid[1])

        draw_polygon_fancy(len(segments))
        draw_points_fancy()

        # New best flash effect
        if new_best_flash > 0.1:
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill((*GOLD[:3], int(new_best_flash * 50)))
            screen.blit(s, (0, 0))

    elif state == State.SHOW_RESULT:
        draw_filled_cells(inside_cells, pulse=True)

        if best_valid:
            draw_best_rect(best_valid[0], best_valid[1])

            # Continuous sparkles
            if random.random() < 0.4:
                sx, sy, w, h = get_rect_screen(best_valid[0], best_valid[1])
                spawn_particles(sx + random.uniform(0, w), sy + random.uniform(0, h), 1, GOLD_BRIGHT, 'star')

        draw_polygon_fancy(len(segments))
        draw_points_fancy(pulse=True)

        # Result display with animation
        result_y = HEIGHT - 110
        bounce = ease_out_elastic(min(animation_time * 2, 1.0))

        # Background panel
        panel_h = 90
        panel_y = result_y - 10
        s = pygame.Surface((WIDTH, panel_h), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        screen.blit(s, (0, panel_y))

        # Answer with glow
        answer_text = f"ANSWER: {best_area:,}"
        answer_render = font_huge.render(answer_text, True, GOLD_BRIGHT)
        answer_x = WIDTH//2 - answer_render.get_width()//2
        answer_y = result_y + int((1 - bounce) * 50)

        # Glow layers
        for i in range(3):
            glow = font_huge.render(answer_text, True, (*GOLD[:3],))
            screen.blit(glow, (answer_x - i, answer_y - i))
            screen.blit(glow, (answer_x + i, answer_y + i))
        screen.blit(answer_render, (answer_x, answer_y))

        stats_text = f"Checked {checked_count:,} rectangles • {valid_count:,} valid"
        stats_render = font_med.render(stats_text, True, TEXT_DIM)
        screen.blit(stats_render, (WIDTH//2 - stats_render.get_width()//2, result_y + 55))

    draw_info()

    # Update and draw particles
    particles[:] = [p for p in particles if p.update(dt)]
    for p in particles:
        p.draw(screen)

    pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                if state == State.INTRO:
                    state = State.DRAW_POLYGON
                    animation_time = 0
            elif event.key == pygame.K_s:
                skip_animation = True
                if state == State.INTRO:
                    state = State.CHECK_RECTS
                    filled_cells = list(inside_cells)
                elif state in (State.DRAW_POLYGON, State.FILL_CELLS):
                    state = State.CHECK_RECTS
                    filled_cells = list(inside_cells)
            elif event.key == pygame.K_r:
                state = State.INTRO
                animation_time = 0
                filled_cells = []
                current_pair_idx = 0
                best_valid = None
                best_area = 0
                checked_count = 0
                valid_count = 0
                particles = []
                skip_animation = False
                speed_multiplier = 1.0
                checking_history.clear()
            elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                speed_multiplier = min(speed_multiplier * 2, 16.0)
            elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                speed_multiplier = max(speed_multiplier / 2, 0.25)

    draw()
    clock.tick(60)

pygame.quit()
sys.exit()
