import pygame
import time
import random

# Initialize Pygame
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Lifelike Eye Simulator")
clock = pygame.time.Clock()

# Colors
EYE_COLOR = (0, 136, 255)
LID_COLOR = (0, 0, 0)
BG_COLOR = (0, 0, 0)

# Eye parameters
eye_width, eye_height = 180, 180
corner_radius = 45
eye_y = HEIGHT // 2 - eye_height // 2
eye_spacing = 300

# Movement positions
positions = {"center": 0, "left": -40, "right": 40}
movement_order = ["center", "left", "center", "right", "center"]
current_index = 0
current_target = positions[movement_order[current_index]]
current_position = 0
move_start_time = time.time()
move_duration = 0.6
rest_duration = random.uniform(4, 7)
moving = False
last_change_time = time.time()

# Blink
blink_start_time = time.time()
blink_duration = 0.1
blink_interval = random.uniform(3, 6)
blinking = False
lid_progress = 0
lid_direction = 1

# Mode states
mode = 1  # 1=normal, 2=distortion
mode_start_time = time.time()
mode_duration = 0
next_mode_time = time.time() + random.uniform(6, 12)

def draw_rounded_eye(surface, x, y, width, height, radius, visible=True):
    if visible:
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, EYE_COLOR, rect, border_radius=radius)

def draw_circle_eye(surface, x, y, diameter, visible=True):
    if visible:
        pygame.draw.ellipse(surface, EYE_COLOR, (x, y, diameter, diameter))

def draw_lid(surface, x, y, width, height, progress):
    lid_height = int(height * progress)
    pygame.draw.rect(surface, LID_COLOR, (x, y, width, lid_height), border_radius=corner_radius)
    lower_y = y + height - lid_height
    pygame.draw.rect(surface, LID_COLOR, (x, lower_y, width, lid_height), border_radius=corner_radius)

def randomize_mode():
    global mode, mode_start_time, mode_duration, next_mode_time
    mode = random.choice([1, 2])
    mode_start_time = time.time()
    mode_duration = 3 + random.uniform(0.5, 1.5) if mode == 2 else 0
    next_mode_time = time.time() + random.uniform(10, 15)

# Main loop
running = True
while running:
    screen.fill(BG_COLOR)
    now = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
           (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Handle mode change
    if now > next_mode_time:
        randomize_mode()

    if mode == 2 and now - mode_start_time > mode_duration:
        mode = 1

    # Eye movement logic
    if not moving and now - last_change_time >= rest_duration:
        current_index = (current_index + 1) % len(movement_order)
        target = positions[movement_order[current_index]]
        move_start_time = now
        start_position = current_position
        delta_position = target - start_position
        moving = True

    if moving:
        t = (now - move_start_time) / move_duration
        if t >= 1.0:
            current_position = positions[movement_order[current_index]]
            moving = False
            last_change_time = now
            rest_duration = random.uniform(4, 7)
        else:
            current_position = start_position + delta_position * t

    # Blink logic
    if not blinking and now - blink_start_time > blink_interval:
        blinking = True
        lid_progress = 0
        lid_direction = 1

    if blinking:
        lid_progress += lid_direction * (clock.get_time() / 1000.0 / blink_duration)
        if lid_progress >= 1:
            lid_progress = 1
            lid_direction = -1
        elif lid_progress <= 0:
            lid_progress = 0
            blinking = False
            blink_start_time = now
            blink_interval = random.uniform(3, 6)

    current_move = movement_order[current_index]

    # Draw eyes
    for i, dx in enumerate([-eye_spacing, eye_spacing]):
        is_left = (i == 0)
        eye_x = WIDTH // 2 + dx - eye_width // 2 + current_position
        draw = True

        if mode == 2:
            # Distortion mode
            if is_left:
                ew, eh = int(eye_width * 1.3), int(eye_height * 1.3)
                ex = eye_x - (ew - eye_width) // 2
                ey = eye_y - (eh - eye_height) // 2
                draw_rounded_eye(screen, ex, ey, ew, eh, corner_radius, draw)
                if blinking:
                    draw_lid(screen, ex, ey, ew, eh, lid_progress)
            else:
                d = min(eye_width, eye_height)
                ex = eye_x + (eye_width - d) // 2
                ey = eye_y + (eye_height - d) // 2
                draw_circle_eye(screen, ex, ey, d, draw)
                if blinking:
                    draw_lid(screen, ex, ey, d, d, lid_progress)

        else:
            if current_move == "left":
                if is_left:
                    # Left eye as circle
                    d = min(eye_width, eye_height)
                    ex = eye_x + (eye_width - d) // 2
                    ey = eye_y + (eye_height - d) // 2
                    draw_circle_eye(screen, ex, ey, d, draw)
                    if blinking:
                        draw_lid(screen, ex, ey, d, d, lid_progress)
                else:
                    # Right eye enlarged
                    ew, eh = int(eye_width * 1.3), int(eye_height * 1.3)
                    ex = eye_x - (ew - eye_width) // 2
                    ey = eye_y - (eh - eye_height) // 2
                    draw_rounded_eye(screen, ex, ey, ew, eh, corner_radius, draw)
                    if blinking:
                        draw_lid(screen, ex, ey, ew, eh, lid_progress)
            elif current_move == "right":
                if not is_left:
                    # Right eye as circle
                    d = min(eye_width, eye_height)
                    ex = eye_x + (eye_width - d) // 2
                    ey = eye_y + (eye_height - d) // 2
                    draw_circle_eye(screen, ex, ey, d, draw)
                    if blinking:
                        draw_lid(screen, ex, ey, d, d, lid_progress)
                else:
                    # Left eye enlarged
                    ew, eh = int(eye_width * 1.3), int(eye_height * 1.3)
                    ex = eye_x - (ew - eye_width) // 2
                    ey = eye_y - (eh - eye_height) // 2
                    draw_rounded_eye(screen, ex, ey, ew, eh, corner_radius, draw)
                    if blinking:
                        draw_lid(screen, ex, ey, ew, eh, lid_progress)
            else:
                # Center: both eyes normal
                draw_rounded_eye(screen, eye_x, eye_y, eye_width, eye_height, corner_radius, draw)
                if blinking:
                    draw_lid(screen, eye_x, eye_y, eye_width, eye_height, lid_progress)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
