import math
import random
import sys

import pygame


# ---------- Config ----------
WIDTH, HEIGHT = 960, 540
FPS = 60

# Car/game parameters
MAX_SPEED = 260.0  # km/h visual only
ACCEL_RATE = 120.0  # km/h per second
BRAKE_RATE = 220.0  # km/h per second
COAST_RATE = 80.0   # km/h per second natural slowdown
STEER_RATE = 2.3    # lane units per second at full input
WHEEL_MAX_VISUAL_DEG = 180  # visual steering wheel rotation limit

# Road parameters
LANE_WIDTH = 1.0
NUM_LANES = 2
ROAD_SEGMENTS = 140
CAMERA_HEIGHT = 1.6
FOCAL_LENGTH = 260.0
HORIZON_Y = int(HEIGHT * 0.42)
ROAD_CURVE_STRENGTH = 0.8  # How much the road curves left/right
ROAD_CURVE_CHANGE_INTERVAL = 8.0  # Seconds between curve direction changes

# Obstacles
SPAWN_INTERVAL = 5  # seconds for traffic
SIDE_OBSTACLE_INTERVAL = 1.8  # seconds for trees/signs
OBSTACLE_SPEED_FACTOR = 1.0  # moves with world relative speed
COURSE_LENGTH = 5000.0  # meters to finish line


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("In-Car Racer")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.SysFont("Segoe UI", 16)
        self.font_medium = pygame.font.SysFont("Segoe UI", 22, bold=True)

        # State
        self.speed_kmh = 0.0
        self.target_speed_kmh = 0.0
        self.lane_offset = 0.0  # -1 ... +1 relative to center lane offsets
        self.steer_input = 0.0  # -1..1
        self.wheel_visual_deg = 0.0
        self.road_scroll = 0.0  # meters along road for lane dash animation
        self.road_curve = 0.0  # -1 to 1, negative = left curve, positive = right curve
        self.curve_timer = 0.0  # Timer for changing curve direction
        self.distance_traveled = 0.0  # Progress towards finish line

        # Obstacles: list of dicts with z (meters), lane (int 0..NUM_LANES-1), x_offset (for slight variation)
        self.obstacles = []
        self.side_obstacles = []  # Trees, signs on road sides
        self.spawn_timer = 0.0
        self.side_spawn_timer = 0.0
        self.score = 0
        self.game_over = False
        self.finished = False

        # Pre-render steering wheel sprite
        self.wheel_base = self._create_steering_wheel_surface(240)

    # ---------- Asset builders ----------
    def _create_steering_wheel_surface(self, diameter: int) -> pygame.Surface:
        radius = diameter // 2
        surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        center = (radius, radius)

        # Outer rim
        pygame.draw.circle(surf, (28, 28, 28), center, radius)
        pygame.draw.circle(surf, (8, 8, 8), center, radius, 10)
        pygame.draw.circle(surf, (70, 70, 70), center, radius - 14, 18)

        # Hub
        pygame.draw.circle(surf, (35, 35, 35), center, 34)
        pygame.draw.circle(surf, (12, 12, 12), center, 34, 6)

        # Spokes (3)
        spoke_color = (50, 50, 50)
        for angle_deg in (90, -30, 210):
            ang = math.radians(angle_deg)
            x1 = center[0] + math.cos(ang) * 30
            y1 = center[1] + math.sin(ang) * 30
            x2 = center[0] + math.cos(ang) * (radius - 22)
            y2 = center[1] + math.sin(ang) * (radius - 22)
            pygame.draw.line(surf, spoke_color, (x1, y1), (x2, y2), 16)
            pygame.draw.line(surf, (22, 22, 22), (x1, y1), (x2, y2), 4)

        # Top center mark
        pygame.draw.circle(surf, (200, 40, 40), (center[0], center[1] - radius + 26), 6)
        return surf

    # ---------- Input ----------
    def handle_input(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        accelerate = keys[pygame.K_w] or keys[pygame.K_UP]
        brake = keys[pygame.K_s] or keys[pygame.K_DOWN]
        steer_left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        steer_right = keys[pygame.K_d] or keys[pygame.K_RIGHT]

        # Target speed
        if accelerate:
            self.target_speed_kmh = MAX_SPEED
        elif brake:
            self.target_speed_kmh = 0.0
        else:
            # maintain current target unless coasting
            self.target_speed_kmh = clamp(self.target_speed_kmh, 0.0, MAX_SPEED)

        # Smooth speed towards target
        if self.speed_kmh < self.target_speed_kmh:
            self.speed_kmh += ACCEL_RATE * dt
        elif self.speed_kmh > self.target_speed_kmh:
            decel = BRAKE_RATE if brake else COAST_RATE
            self.speed_kmh -= decel * dt
        self.speed_kmh = clamp(self.speed_kmh, 0.0, MAX_SPEED)

        # Steering input
        input_axis = 0.0
        if steer_left:
            input_axis -= 1.0
        if steer_right:
            input_axis += 1.0
        # Smooth input
        self.steer_input = self._smooth_damp(self.steer_input, input_axis, 10.0, dt)

        # Update lane offset based on steer and speed (more speed -> less agile)
        speed_factor = 0.4 + 0.6 * (1.0 - (self.speed_kmh / MAX_SPEED))
        # Add road curve influence on steering
        curve_influence = self.road_curve * 0.3 * speed_factor
        self.lane_offset += (self.steer_input * STEER_RATE + curve_influence) * speed_factor * dt
        # clamp to road width edges
        max_offset = (NUM_LANES - 1) * 0.5
        self.lane_offset = clamp(self.lane_offset, -max_offset, max_offset)

        # Update steering wheel visual angle with smoothing
        target_wheel_deg = self.steer_input * WHEEL_MAX_VISUAL_DEG
        self.wheel_visual_deg = self._lerp(self.wheel_visual_deg, target_wheel_deg, 1.0 - math.pow(0.001, dt))

    # ---------- Update ----------
    def update(self, dt: float) -> None:
        # Advance road scroll
        meters_per_sec = self.speed_kmh / 3.6
        self.road_scroll += meters_per_sec * dt
        self.distance_traveled += meters_per_sec * dt

        # Update road curve
        self.curve_timer -= dt
        if self.curve_timer <= 0.0:
            self.curve_timer = ROAD_CURVE_CHANGE_INTERVAL * (0.7 + random.random() * 0.8)
            # Smoothly change curve direction
            target_curve = random.uniform(-1.0, 1.0)
            self.road_curve = self._lerp(self.road_curve, target_curve, 0.3)

        # Check if finished
        if self.distance_traveled >= COURSE_LENGTH and not self.finished:
            self.finished = True
            self.target_speed_kmh = 0.0

        # Spawn obstacles
        self.spawn_timer -= dt
        if self.spawn_timer <= 0.0 and not self.game_over:
            self.spawn_timer = SPAWN_INTERVAL * (0.7 + random.random() * 0.8)
            lane = random.randrange(NUM_LANES)
            z = 140.0 + random.random() * 80.0
            offset_variation = (random.random() - 0.5) * 0.3
            self.obstacles.append({
                "z": z,
                "lane": lane,
                "x_offset": offset_variation,
                "w": 0.9,
                "h": 0.6,
                "type": "car",
                "color": (random.choice([(200, 50, 50), (50, 50, 200), (50, 200, 50), (200, 200, 50)]))
            })

        # Spawn side obstacles (trees, signs)
        self.side_spawn_timer -= dt
        if self.side_spawn_timer <= 0.0 and not self.game_over:
            self.side_spawn_timer = SIDE_OBSTACLE_INTERVAL * (0.6 + random.random() * 0.8)
            side = random.choice([-1, 1])  # Left or right side
            z = 120.0 + random.random() * 60.0
            obstacle_type = random.choice(["tree", "sign"])
            self.side_obstacles.append({
                "z": z,
                "side": side,
                "type": obstacle_type,
                "x_offset": side * (1.8 + random.random() * 0.4),  # Distance from road edge
                "w": 0.8 if obstacle_type == "tree" else 0.4,
                "h": 1.2 if obstacle_type == "tree" else 0.8,
                "color": (34, 139, 34) if obstacle_type == "tree" else (255, 215, 0)
            })

        # Move obstacles towards camera
        new_list = []
        for ob in self.obstacles:
            ob["z"] -= meters_per_sec * dt * OBSTACLE_SPEED_FACTOR
            if ob["z"] > 0.5:  # still ahead
                new_list.append(ob)
            else:
                self.score += 1
        self.obstacles = new_list

        # Move side obstacles
        new_side_list = []
        for ob in self.side_obstacles:
            ob["z"] -= meters_per_sec * dt * OBSTACLE_SPEED_FACTOR
            if ob["z"] > 0.5:
                new_side_list.append(ob)
        self.side_obstacles = new_side_list

        # Collision check
        if not self.game_over:
            for ob in self.obstacles:
                if 2.0 < ob["z"] < 8.0:
                    lane_center = (ob["lane"] - (NUM_LANES - 1) * 0.5) * LANE_WIDTH
                    dx = (self.lane_offset * LANE_WIDTH) - (lane_center + ob["x_offset"])
                    overlap_x = abs(dx) < (LANE_WIDTH * 0.45)
                    if overlap_x:
                        self.game_over = True
                        self.target_speed_kmh = 0.0
                        break

            # Check side obstacle collisions (only if way off road)
            for ob in self.side_obstacles:
                if 1.5 < ob["z"] < 6.0:
                    # Check if car is too far off road
                    if abs(self.lane_offset) > 0.8:  # Car is off road
                        self.game_over = True
                        self.target_speed_kmh = 0.0
                        break

    # ---------- Rendering ----------
    def draw(self) -> None:
        self.screen.fill((27, 32, 48))

        # Sky
        pygame.draw.rect(self.screen, (35, 94, 160), pygame.Rect(0, 0, WIDTH, HORIZON_Y))
        # Distant mountains
        #self._draw_mountains()

        # Road and world
        self._draw_road()
        self._draw_obstacles()
        self._draw_side_obstacles()
        self._draw_finish_line()

        # Cockpit overlay
        self._draw_dashboard()
        self._draw_speedometer()
        self._draw_gear_and_score()

        if self.game_over or self.finished:
            self._draw_game_over()

        pygame.display.flip()

    # ---------- Drawing helpers ----------
    def _project(self, world_x: float, world_y: float, world_z: float) -> tuple[int, int, float]:
        # Simple perspective projection to screen space
        scale = FOCAL_LENGTH / (world_z + CAMERA_HEIGHT)
        x = int(WIDTH / 2 + world_x * scale)
        y = int(HORIZON_Y + world_y * scale)
        return x, y, scale

    def _draw_mountains(self) -> None:
        base_y = HORIZON_Y
        color = (52, 72, 98)
        # Slight parallax shift based on car lateral position
        parallax = int(-self.lane_offset * 40)
        for i in range(3):
            offset = i * 70
            points = [
                (0 + parallax // (i + 1), base_y + 20 + offset),
                (180 + parallax // (i + 1), base_y - 30 + offset),
                (360 + parallax // (i + 1), base_y + 25 + offset),
                (540 + parallax // (i + 1), base_y - 20 + offset),
                (720 + parallax // (i + 1), base_y + 22 + offset),
                (900 + parallax // (i + 1), base_y - 26 + offset),
                (WIDTH + parallax // (i + 1), base_y + 20 + offset),
            ]
            pygame.draw.polygon(self.screen, (color[0], color[1], color[2] - i * 10), points)

    def _draw_road(self) -> None:
        # Road body
        road_color = (40, 40, 40)
        shoulder_color = (70, 70, 70)
        lane_color = (230, 230, 230)
        center_line_color = (255, 255, 255)

        # Draw trapezoids from bottom to horizon for a simple perspective road
        prev_w = WIDTH * 1.2
        prev_y = HEIGHT
        # Shift road center opposite to lane offset (camera pans with the car)
        # Add road curve offset
        curve_offset = int(self.road_curve * 120)
        center_x = WIDTH // 2 - int(self.lane_offset * 180) + curve_offset
        for i in range(ROAD_SEGMENTS):
            z0 = i * 2.0 + (self.road_scroll % 2.0)
            z1 = (i + 1) * 2.0 + (self.road_scroll % 2.0)

            x0, y0, s0 = self._project(0, 0, z0)
            x1, y1, s1 = self._project(0, 0, z1)

            road_w0 = int(s0 * (NUM_LANES * LANE_WIDTH) * 180)
            road_w1 = int(s1 * (NUM_LANES * LANE_WIDTH) * 180)

            # Shoulders
            shoulder_w0 = int(road_w0 * 1.15)
            shoulder_w1 = int(road_w1 * 1.15)
            pygame.draw.polygon(
                self.screen,
                shoulder_color,
                [
                    (center_x - shoulder_w0, y0),
                    (center_x + shoulder_w0, y0),
                    (center_x + shoulder_w1, y1),
                    (center_x - shoulder_w1, y1),
                ],
            )

            # Road
            pygame.draw.polygon(
                self.screen,
                road_color,
                [
                    (center_x - road_w0, y0),
                    (center_x + road_w0, y0),
                    (center_x + road_w1, y1),
                    (center_x - road_w1, y1),
                ],
            )

            # Center line (dotted) - draw AFTER road so it's visible
            if i % 2 == 0:  # Dashed line
                pygame.draw.polygon(
                    self.screen,
                    center_line_color,
                    [
                        (center_x - 4, y0),
                        (center_x + 4, y0),
                        (center_x + 3, y1),
                        (center_x - 3, y1),
                    ],
                )

            # Solid white lines on edges - draw AFTER road so they're visible
            edge_width = 3
            # Left edge
            pygame.draw.polygon(
                self.screen,
                lane_color,
                [
                    (center_x - road_w0 - edge_width, y0),
                    (center_x - road_w0, y0),
                    (center_x - road_w1, y1),
                    (center_x - road_w1 - edge_width, y1),
                ],
            )
            # Right edge
            pygame.draw.polygon(
                self.screen,
                lane_color,
                [
                    (center_x + road_w0, y0),
                    (center_x + road_w0 + edge_width, y0),
                    (center_x + road_w1 + edge_width, y1),
                    (center_x + road_w1, y1),
                ],
            )

            prev_w = road_w1
            prev_y = y1

        # Apply camera lateral offset to simulate car movement: draw a dark vignette mask
        #vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        #dark = (0, 0, 0, 110)
        #pygame.draw.rect(vignette, dark, pygame.Rect(0, HORIZON_Y, WIDTH, HEIGHT - HORIZON_Y))
        #self.screen.blit(vignette, (0, 0))

    def _draw_obstacles(self) -> None:
        for ob in sorted(self.obstacles, key=lambda o: -o["z"]):
            lane_center = (ob["lane"] - (NUM_LANES - 1) * 0.5) * LANE_WIDTH
            # Offset obstacles by camera lateral position so scene moves when steering
            world_x = (lane_center + ob["x_offset"] - self.lane_offset * LANE_WIDTH) * 180
            x, y, scale = self._project(world_x, 0, ob["z"])
            w = max(6, int(ob["w"] * 100 * scale))
            h = max(6, int(ob["h"] * 100 * scale))
            # Draw car with Mario Kart style
            if ob["type"] == "car":
                # Car body
                pygame.draw.rect(self.screen, ob["color"], pygame.Rect(x - w//2, y - h, w, h), border_radius=8)
                pygame.draw.rect(self.screen, (20, 20, 20), pygame.Rect(x - w//2, y - h, w, h), 2, border_radius=8)
                # Windows
                window_w = int(w * 0.6)
                window_h = int(h * 0.4)
                pygame.draw.rect(self.screen, (135, 206, 235), pygame.Rect(x - window_w//2, y - h + 2, window_w, window_h), border_radius=4)
                pygame.draw.rect(self.screen, (20, 20, 20), pygame.Rect(x - window_w//2, y - h + 2, window_w, window_h), 1, border_radius=4)

    def _draw_side_obstacles(self) -> None:
        for ob in sorted(self.side_obstacles, key=lambda o: -o["z"]):
            # Offset by camera lateral position and road curve
            curve_offset = int(self.road_curve * 120)
            world_x = (ob["x_offset"] - self.lane_offset * LANE_WIDTH) * 180 + curve_offset
            x, y, scale = self._project(world_x, 0, ob["z"])
            w = max(6, int(ob["w"] * 100 * scale))
            h = max(6, int(ob["h"] * 100 * scale))

            if ob["type"] == "tree":
                # Tree trunk
                trunk_w = max(3, int(w * 0.3))
                trunk_h = int(h * 0.6)
                trunk_rect = pygame.Rect(x - trunk_w//2, y - trunk_h//2, trunk_w, trunk_h)
                pygame.draw.rect(self.screen, (139, 69, 19), trunk_rect)
                # Tree top (leaves)
                leaf_w = w
                leaf_h = int(h * 0.7)
                leaf_rect = pygame.Rect(x - leaf_w//2, y - h, leaf_w, leaf_h)
                pygame.draw.ellipse(self.screen, ob["color"], leaf_rect)
                pygame.draw.ellipse(self.screen, (20, 20, 20), leaf_rect, 2)
            else:  # Sign
                # Sign post
                post_w = max(2, int(w * 0.2))
                post_h = h
                pygame.draw.rect(self.screen, (139, 69, 19), pygame.Rect(x - post_w//2, y - h//2, post_w, post_h))
                # Sign board
                sign_w = w
                sign_h = int(h * 0.6)
                sign_rect = pygame.Rect(x - sign_w//2, y - h, sign_w, sign_h)
                pygame.draw.rect(self.screen, ob["color"], sign_rect, border_radius=4)
                pygame.draw.rect(self.screen, (20, 20, 20), sign_rect, 2, border_radius=4)

    def _draw_finish_line(self) -> None:
        # Check if finish line should be visible
        if self.distance_traveled < COURSE_LENGTH - 100:  # Show when within 100m
            return

        # Draw checkered banner arch
        banner_z = COURSE_LENGTH - self.distance_traveled
        if banner_z > 0:
            x, y, scale = self._project(0, 0, banner_z)
            banner_w = int(200 * scale)
            banner_h = int(80 * scale)
            
            # Banner arch
            arch_rect = pygame.Rect(x - banner_w//2, y - banner_h, banner_w, banner_h)
            # Checkered pattern
            check_size = max(8, int(20 * scale))
            for i in range(0, banner_w, check_size):
                for j in range(0, banner_h, check_size):
                    color = (255, 255, 255) if (i + j) // check_size % 2 == 0 else (0, 0, 0)
                    pygame.draw.rect(self.screen, color, pygame.Rect(x - banner_w//2 + i, y - banner_h + j, check_size, check_size))
            
            # FINISH text
            if scale > 0.1:  # Only show text when close enough
                text_size = max(16, int(40 * scale))
                font = pygame.font.SysFont("Arial", text_size, bold=True)
                finish_text = font.render("FINISH", True, (255, 0, 0))
                text_rect = finish_text.get_rect(center=(x, y - banner_h//2))
                self.screen.blit(finish_text, text_rect)

    def _draw_dashboard(self) -> None:
        # Dashboard panel
        dash_rect = pygame.Rect(0, int(HEIGHT * 0.70), WIDTH, int(HEIGHT * 0.30))
        pygame.draw.rect(self.screen, (18, 18, 18), dash_rect)
        pygame.draw.rect(self.screen, (8, 8, 8), dash_rect, 6)

        # Steering wheel
        rotated = pygame.transform.rotozoom(self.wheel_base, -self.wheel_visual_deg, 1.0)
        wheel_rect = rotated.get_rect()
        wheel_rect.center = (WIDTH // 2, int(HEIGHT * 0.94))
        self.screen.blit(rotated, wheel_rect)

    def _draw_speedometer(self) -> None:
        # Gauge container
        center = (int(WIDTH * 0.86), int(HEIGHT * 0.86))
        radius = 80
        pygame.draw.circle(self.screen, (24, 24, 24), center, radius + 18)
        pygame.draw.circle(self.screen, (10, 10, 10), center, radius + 18, 6)
        pygame.draw.circle(self.screen, (30, 30, 30), center, radius)
        pygame.draw.circle(self.screen, (12, 12, 12), center, radius, 4)

        # Ticks and labels
        start_angle = math.radians(210)
        end_angle = math.radians(-30)
        num_ticks = 13  # 0..260 every 20
        for i in range(num_ticks):
            t = i / (num_ticks - 1)
            ang = start_angle + (end_angle - start_angle) * t
            outer = radius - 6
            inner = radius - (18 if i % 2 == 0 else 12)
            x0 = center[0] + math.cos(ang) * inner
            y0 = center[1] + math.sin(ang) * inner
            x1 = center[0] + math.cos(ang) * outer
            y1 = center[1] + math.sin(ang) * outer
            pygame.draw.line(self.screen, (220, 220, 220), (x0, y0), (x1, y1), 2)
            if i % 2 == 0:
                label_speed = i * 20
                txt = self.font_small.render(str(label_speed), True, (220, 220, 220))
                lx = center[0] + math.cos(ang) * (inner - 20) - txt.get_width() / 2
                ly = center[1] + math.sin(ang) * (inner - 20) - txt.get_height() / 2
                self.screen.blit(txt, (lx, ly))

        # Needle
        t = self.speed_kmh / MAX_SPEED
        ang = start_angle + (end_angle - start_angle) * t
        nx = center[0] + math.cos(ang) * (radius - 24)
        ny = center[1] + math.sin(ang) * (radius - 24)
        pygame.draw.line(self.screen, (230, 60, 60), center, (nx, ny), 4)
        pygame.draw.circle(self.screen, (200, 200, 200), center, 6)

        # Digital speed readout
        spd_txt = self.font_medium.render(f"{int(self.speed_kmh + 0.5)}", True, (240, 240, 240))
        unit_txt = self.font_small.render("km/h", True, (200, 200, 200))
        self.screen.blit(spd_txt, (center[0] - spd_txt.get_width() // 2, center[1] + 12))
        self.screen.blit(unit_txt, (center[0] - unit_txt.get_width() // 2, center[1] + 12 + spd_txt.get_height()))

    def _draw_gear_and_score(self) -> None:
        # Simple PRND indicator (fake based on speed target)
        gear = "D" if self.target_speed_kmh > 0.1 else ("N" if self.speed_kmh > 0.1 else "P")
        txt = self.font_medium.render(f"Gear {gear}", True, (230, 230, 230))
        self.screen.blit(txt, (int(WIDTH * 0.07), int(HEIGHT * 0.82)))

        score_txt = self.font_medium.render(f"Score {self.score}", True, (230, 230, 230))
        self.screen.blit(score_txt, (int(WIDTH * 0.07), int(HEIGHT * 0.86)))

        # Progress bar
        progress = self.distance_traveled / COURSE_LENGTH
        progress_bar_w = 200
        progress_bar_h = 20
        progress_x = int(WIDTH * 0.07)
        progress_y = int(HEIGHT * 0.90)
        
        # Background
        pygame.draw.rect(self.screen, (40, 40, 40), pygame.Rect(progress_x, progress_y, progress_bar_w, progress_bar_h))
        pygame.draw.rect(self.screen, (80, 80, 80), pygame.Rect(progress_x, progress_y, progress_bar_w, progress_bar_h), 2)
        # Progress fill
        fill_w = int(progress_bar_w * progress)
        if fill_w > 0:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(progress_x, progress_y, fill_w, progress_bar_h))

        hint = self.font_small.render("W/S accelerate/brake, A/D steer. R to restart, Esc to quit.", True, (200, 200, 200))
        self.screen.blit(hint, (int(WIDTH * 0.07), int(HEIGHT * 0.91)))

    def _draw_game_over(self) -> None:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))
        if self.finished:
            txt = self.font_medium.render("FINISHED! Press R to restart.", True, (0, 255, 0))
        else:
            txt = self.font_medium.render("Crashed! Press R to restart.", True, (255, 220, 220))
        self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 20))

    # ---------- Utils ----------
    def _lerp(self, a: float, b: float, t: float) -> float:
        return a + (b - a) * clamp(t, 0.0, 1.0)

    def _smooth_damp(self, current: float, target: float, speed: float, dt: float) -> float:
        # simple critically-damped smoothing
        return current + (target - current) * clamp(speed * dt, 0.0, 1.0)

    # ---------- Loop ----------
    def run(self) -> None:
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit(0)
                    if event.key == pygame.K_r:
                        self.__init__()  # quick reset

            if not self.game_over:
                self.handle_input(dt)
                self.update(dt)

            self.draw()


if __name__ == "__main__":
    try:
        Game().run()
    except Exception as exc:
        pygame.quit()
        raise


