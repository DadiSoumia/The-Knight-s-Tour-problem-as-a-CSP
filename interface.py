import pygame
import sys
import time
from knighttour import solve_knights_tour

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1000, 650
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knight's Quest — Knight's Tour UI (Final)")
CLOCK = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BG_TOP = (255, 231, 250)
BG_BOTTOM = (238, 219, 255)

# Grid squares
GRID_LIGHT = (254, 202, 255)  # Light pink initial
GRID_DARK = (232, 180, 255)   # Light violet initial
GRID_LIGHT_NUM = (255, 157, 240)  # Darker pink when number placed
GRID_DARK_NUM = (207, 141, 244)   # Darker violet when number placed

# Borders
PRETTY_PINK = (255, 120, 180)  
BORDER_COLOR = PRETTY_PINK

# Knight
KNIGHT_COLOR = (132, 116, 246)
KNIGHT_NUM_COLOR = WHITE

# Numbers
NUM_COLOR = (100, 50, 150) 

# Background overlays
DARK_PINK_OVERLAY = (255, 144, 235)
DARK_PURPLE_OVERLAY = (200, 130, 240)

# Buttons
BUTTON_BASE = (194, 139, 255)
BUTTON_ACCENT = (223, 170, 255)
BUTTON_TEXT = WHITE

# Axes numbers
AXIS_NUM_COLOR = (70, 40, 120)

# ---- Fonts ----
TITLE_FONT = pygame.font.SysFont("comicsansms", 56, bold=True)
SUBTITLE_FONT = pygame.font.SysFont("comicsansms", 24)
BUTTON_FONT = pygame.font.SysFont("comicsansms", 28, bold=True)
SMALL_BUTTON_FONT = pygame.font.SysFont("comicsansms", 20, bold=True)
SMALL_FONT = pygame.font.SysFont("comicsansms", 18)
GRID_NUM_FONT = pygame.font.SysFont("comicsansms", 20, bold=True)
INFO_FONT = pygame.font.SysFont("comicsansms", 17, bold=True)

def draw_rounded_rect(surface, rect, color, radius=12, width=0):
    pygame.draw.rect(surface, color, rect, border_radius=radius, width=width)

def vertical_gradient(surf, rect, top_color, bottom_color):
    x, y, w, h = rect
    grad_surf = pygame.Surface((w, h))
    for i in range(h):
        t = i / max(h - 1, 1)
        r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
        g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
        b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
        pygame.draw.line(grad_surf, (r, g, b), (0, i), (w - 1, i))
    surf.blit(grad_surf, (x, y))

class Button:
    def __init__(self, x, y, w, h, text, base_color=BUTTON_BASE, accent=BUTTON_ACCENT, font=BUTTON_FONT):
        self.base_rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.base_color = base_color
        self.accent = accent
        self.font = font
        self.radius = 16
        self.hover_scale = 1.04

    def draw(self, surf):
        hover = self.base_rect.collidepoint(pygame.mouse.get_pos())
        if hover:
            w = int(self.base_rect.w * self.hover_scale)
            h = int(self.base_rect.h * self.hover_scale)
            x = self.base_rect.centerx - w // 2
            y = self.base_rect.centery - h // 2
            rect = pygame.Rect(x, y, w, h)
        else:
            rect = self.base_rect

        shadow = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 35), (0, 6, rect.w, rect.h - 6), border_radius=self.radius)
        surf.blit(shadow, (rect.x, rect.y))

        draw_rounded_rect(surf, rect, self.base_color, radius=self.radius)
        pygame.draw.rect(surf, PRETTY_PINK, rect, width=2, border_radius=self.radius)

        txt = self.font.render(self.text, True, BUTTON_TEXT)
        surf.blit(txt, (rect.x + (rect.w - txt.get_width())//2, rect.y + (rect.h - txt.get_height())//2))
        return rect

    def is_clicked(self, event_pos):
        return self.base_rect.collidepoint(event_pos)

STATIC_SHAPES = [
    ("circle", BUTTON_ACCENT, 110, 120, int(56 * 0.85)),
    ("circle", GRID_DARK, 240, 90, int(36 * 0.85)),
    ("circle", BUTTON_BASE, 880, 120, int(68 * 0.85)),
    ("circle", GRID_LIGHT, 760, 220, int(48 * 0.85)),
    ("circle", GRID_DARK, 540, 160, int(24 * 0.85)),
    ("circle", BUTTON_BASE, 160, 480, int(40 * 0.85)),
    ("circle", BUTTON_ACCENT, 420, 520, int(30 * 0.85)),
    ("circle", (120, 180, 255), 300, 200, int(35 * 0.85)),
    ("circle", (100, 150, 255), 700, 400, int(50 * 0.85)),
    ("circle", (80, 140, 255), 500, 100, int(25 * 0.85)),
]

def draw_soft_circle(target_surf, color, center, radius, alpha=110):
    if len(color) == 3:
        r, g, b = color
        a = alpha
    else:
        r, g, b, a = color
    size = radius * 2
    circle_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(circle_surf, (r, g, b, a), (radius, radius), radius)
    target_surf.blit(circle_surf, (center[0] - radius, center[1] - radius))

def get_direction_info(from_pos, to_pos):
    """Get the direction index and simple description"""
    fy, fx = from_pos
    ty, tx = to_pos
    dy, dx = ty - fy, tx - fx
    
    knight_moves = [
        ((2, 1), "2 down 1 right", 0),
        ((1, 2), "1 down 2 right", 1),
        ((-1, 2), "1 up 2 right", 2),
        ((-2, 1), "2 up 1 right", 3),
        ((-2, -1), "2 up 1 left", 4),
        ((-1, -2), "1 up 2 left", 5),
        ((1, -2), "1 down 2 left", 6),
        ((2, -1), "2 down 1 left", 7),
    ]
    
    for (mdy, mdx), name, idx in knight_moves:
        if dy == mdy and dx == mdx:
            return idx, name
    return None, None

# ---- Menu Page ----
def menu_page():
    start_btn = Button(WIDTH//2 - 170, 320, 340, 72, "PLAY", base_color=(196, 123, 255), accent=(223, 170, 255))
    quit_btn = Button(WIDTH//2 - 170, 410, 340, 64, "QUIT", base_color=(255, 120, 180), accent=(255, 160, 210))

    while True:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_btn.is_clicked(event.pos):
                    return "grid"
                if quit_btn.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()

        vertical_gradient(SCREEN, (0, 0, WIDTH, HEIGHT), BG_TOP, BG_BOTTOM)

        for kind, color, cx, cy, size in STATIC_SHAPES:
            if kind == "circle":
                draw_soft_circle(SCREEN, color, (cx, cy), size, alpha=100)

        title_text = "KNIGHT'S QUEST"
        glow = TITLE_FONT.render(title_text, True, (255, 200, 240))
        title_surf = TITLE_FONT.render(title_text, True, (70, 40, 120))
        SCREEN.blit(glow, ((WIDTH - glow.get_width())//2 + 4, 62 + 4))
        SCREEN.blit(title_surf, ((WIDTH - title_surf.get_width())//2, 62))

        sub = SUBTITLE_FONT.render("a pastel knight's tour demo", True, (110, 60, 150))
        SCREEN.blit(sub, ((WIDTH - sub.get_width())//2, 130))

        start_btn.draw(SCREEN)
        quit_btn.draw(SCREEN)

        hint = SMALL_FONT.render("Click PLAY to open the board. Hover the buttons for effect.", True, (90, 60, 120))
        SCREEN.blit(hint, ((WIDTH - hint.get_width())//2, HEIGHT - 68))

        pygame.display.flip()

import threading

def grid_page():
    grid_n = 8
    cell_size = 50
    board_width = grid_n * cell_size
    board_height = grid_n * cell_size
    board_x = (WIDTH - board_width) // 2
    board_y = (HEIGHT - board_height) // 2 + 20

    # ⚡ Boutons existants
    back_btn = Button(16, 18, 110, 44, "BACK", base_color=(120, 180, 255), accent=(160, 200, 255), font=SMALL_BUTTON_FONT)
    pause_btn = Button(16, 74, 110, 44, "PAUSE", base_color=(165, 100, 255), accent=(200, 140, 255), font=SMALL_BUTTON_FONT)
    reset_btn = Button(16, 130, 110, 44, "RESET", base_color=(255, 120, 180), accent=(255, 150, 210), font=SMALL_BUTTON_FONT)
    heuristic_btn = Button(16, 186, 180, 44, "HEURISTIC ON", base_color=(150, 200, 255), accent=(180, 220, 255), font=SMALL_BUTTON_FONT)

    paused = False
    start_time = time.time()
    paused_time = None
    total_paused_duration = 0.0
    current_step = 0
    step_delay = 0.5
    last_step_time = time.time()
    current_direction_name = None
    use_heuristic = True  # par défaut
    best_knight = None
    solution_ready = False

    # --- Fonction pour calculer la solution dans un thread ---
    def compute_solution():
        nonlocal best_knight, solution_ready
        sol = solve_knights_tour(use_heuristic)
        best_knight = type('Obj', (object,), {})()
        best_knight.path = [(r, c, str(i+1)) for i, (r, c) in enumerate(sol)]
        solution_ready = True

    # Lancer le thread
    threading.Thread(target=compute_solution, daemon=True).start()

    while True:
        CLOCK.tick(FPS)
        now = time.time()

        # --- Gestion des événements ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.is_clicked(event.pos):
                    return "menu"
                if pause_btn.is_clicked(event.pos):
                    paused = not paused
                    pause_btn.text = "RESUME" if paused else "PAUSE"
                    if paused:
                        paused_time = now
                    else:
                        if paused_time is not None:
                            total_paused_duration += now - paused_time
                        paused_time = None
                if reset_btn.is_clicked(event.pos):
                    current_step = 0
                    last_step_time = now
                    paused = False
                    pause_btn.text = "PAUSE"
                    current_direction_name = None
                    # Recalculer la solution dans un nouveau thread
                    solution_ready = False
                    best_knight = None
                    threading.Thread(target=compute_solution, daemon=True).start()
                if heuristic_btn.is_clicked(event.pos):
                    use_heuristic = not use_heuristic
                    heuristic_btn.text = "HEURISTIC ON" if use_heuristic else "HEURISTIC OFF"
                    # Recalculer la solution avec la nouvelle option
                    solution_ready = False
                    best_knight = None
                    threading.Thread(target=compute_solution, daemon=True).start()

        # --- Avancer le chevalier étape par étape ---
        if not paused and best_knight and best_knight.path:
            if now - last_step_time >= step_delay and current_step < len(best_knight.path):
                if current_step > 0:
                    prev_pos = best_knight.path[current_step - 1][:2]
                    curr_pos = best_knight.path[current_step][:2]
                    _, current_direction_name = get_direction_info(prev_pos, curr_pos)
                current_step += 1
                last_step_time = now

        # --- Dessiner fond et grille ---
        vertical_gradient(SCREEN, (0, 0, WIDTH, HEIGHT), BG_TOP, BG_BOTTOM)
        for r in range(grid_n):
            for c in range(grid_n):
                rect = pygame.Rect(board_x + c*cell_size, board_y + r*cell_size, cell_size, cell_size)
                is_light = (r + c) % 2 == 0
                base_color = GRID_LIGHT if is_light else GRID_DARK
                draw_rounded_rect(SCREEN, rect, base_color, radius=6)
                pygame.draw.rect(SCREEN, PRETTY_PINK, rect, width=2, border_radius=6)

        
        # --- Afficher axes ---
        for i in range(grid_n):
            idx_surf = SMALL_FONT.render(str(i+1), True, AXIS_NUM_COLOR)
            SCREEN.blit(idx_surf, (board_x - 30, board_y + i*cell_size + (cell_size - idx_surf.get_height())//2))
            SCREEN.blit(idx_surf, (board_x + board_width + 12, board_y + i*cell_size + (cell_size - idx_surf.get_height())//2))
            SCREEN.blit(idx_surf, (board_x + i*cell_size + (cell_size - idx_surf.get_width())//2, board_y - 28))
            SCREEN.blit(idx_surf, (board_x + i*cell_size + (cell_size - idx_surf.get_width())//2, board_y + board_height + 8))

        # --- Afficher chemin du chevalier ---
        if best_knight:
            for idx in range(current_step):
                r, c, label = best_knight.path[idx]
                rect = pygame.Rect(board_x + c*cell_size, board_y + r*cell_size, cell_size, cell_size)
                is_light = (r + c) % 2 == 0
                overlay_color = GRID_LIGHT_NUM if is_light else GRID_DARK_NUM
                overlay_surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                overlay_surf.fill((*overlay_color, 200))
                SCREEN.blit(overlay_surf, rect.topleft)

                txt = GRID_NUM_FONT.render(label, True, WHITE)
                SCREEN.blit(txt, (rect.x + (cell_size - txt.get_width())//2, rect.y + (cell_size - txt.get_height())//2))

        # --- Dessiner boutons et infos ---
        back_btn.draw(SCREEN)
        pause_btn.draw(SCREEN)
        reset_btn.draw(SCREEN)
        heuristic_btn.draw(SCREEN)

        # --- Afficher steps et direction ---
        info_w, info_h = 200, 60
        info_x = WIDTH - info_w - 20
        info_y = 20

        steps_y = info_y + info_h + 12
        pygame.draw.rect(SCREEN, WHITE, (info_x, steps_y, info_w, info_h), border_radius=12)
        pygame.draw.rect(SCREEN, PRETTY_PINK, (info_x, steps_y, info_w, info_h), width=2, border_radius=12)
        steps_label = INFO_FONT.render("STEPS", True, AXIS_NUM_COLOR)
        steps_val = INFO_FONT.render(str(current_step), True, AXIS_NUM_COLOR)
        SCREEN.blit(steps_label, (info_x + 12, steps_y + 8))
        SCREEN.blit(steps_val, (info_x + 12, steps_y + 32))

        dir_y = steps_y + info_h + 12
        pygame.draw.rect(SCREEN, WHITE, (info_x, dir_y, info_w, info_h), border_radius=12)
        pygame.draw.rect(SCREEN, PRETTY_PINK, (info_x, dir_y, info_w, info_h), width=2, border_radius=12)
        dir_label = INFO_FONT.render("DIRECTION", True, AXIS_NUM_COLOR)
        dir_text = current_direction_name if current_direction_name else "—"
        dir_val = INFO_FONT.render(dir_text, True, AXIS_NUM_COLOR)
        SCREEN.blit(dir_label, (info_x + 12, dir_y + 8))
        SCREEN.blit(dir_val, (info_x + 12, dir_y + 32))

        pygame.display.flip()


def main():
    page = "menu"
    while True:
        if page == "menu":
            page = menu_page()
        elif page == "grid":
            page = grid_page()
        else:
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
    
