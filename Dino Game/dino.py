"""
Simple Dino Game (like Chrome's offline T-Rex game)
Controls:
  SPACE / UP  -> Jump
  DOWN        -> Duck
  R           -> Restart after game over
  ESC         -> Quit
"""

import pygame
import random
import sys

pygame.init()

# ---------- Settings ----------
WIDTH, HEIGHT = 800, 300
GROUND_Y = 250
FPS = 60

WHITE = (255, 255, 255)
BLACK = (40, 40, 40)
GRAY = (200, 200, 200)
RED = (200, 30, 30)

GRAVITY = 0.9
JUMP_STRENGTH = -15

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Dino Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 22)
big_font = pygame.font.SysFont("consolas", 36, bold=True)


class Dino:
    def __init__(self):
        self.width = 44
        self.height_stand = 47
        self.height_duck = 25
        self.x = 50
        self.y = GROUND_Y - self.height_stand
        self.vel_y = 0
        self.ducking = False
        self.on_ground = True
        self.leg_frame = 0
        self.leg_timer = 0

    @property
    def height(self):
        return self.height_duck if self.ducking else self.height_stand

    @property
    def rect(self):
        return pygame.Rect(self.x, GROUND_Y - self.height, self.width, self.height)

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False

    def duck(self, is_ducking):
        if self.on_ground:
            self.ducking = is_ducking

    def update(self):
        self.vel_y += GRAVITY
        self.y_offset = 0
        if not self.on_ground:
            self.ducking = False

        top = GROUND_Y - self.height
        # simulate vertical position via vel_y applied to a "float" tracked separately
        self._apply_gravity()

        # simple leg animation
        self.leg_timer += 1
        if self.leg_timer > 6:
            self.leg_timer = 0
            self.leg_frame = 1 - self.leg_frame

    def _apply_gravity(self):
        # track actual y position with gravity
        if not hasattr(self, "pos_y"):
            self.pos_y = GROUND_Y - self.height
        self.pos_y += self.vel_y
        if self.pos_y >= GROUND_Y - self.height:
            self.pos_y = GROUND_Y - self.height
            self.vel_y = 0
            self.on_ground = True

    def draw(self, surface):
        r = pygame.Rect(self.x, self.pos_y if hasattr(self, "pos_y") else self.y,
                         self.width, self.height)
        pygame.draw.rect(surface, BLACK, r, border_radius=4)
        # eye
        eye_x = self.x + self.width - 10
        eye_y = int(r.y) + 8
        pygame.draw.circle(surface, WHITE, (eye_x, eye_y), 3)
        # legs (simple animation, only when on ground and not ducking)
        if self.on_ground and not self.ducking:
            leg_y = r.bottom
            if self.leg_frame == 0:
                pygame.draw.line(surface, BLACK, (r.x + 10, leg_y), (r.x + 6, leg_y + 8), 4)
                pygame.draw.line(surface, BLACK, (r.x + 30, leg_y), (r.x + 34, leg_y + 8), 4)
            else:
                pygame.draw.line(surface, BLACK, (r.x + 10, leg_y), (r.x + 14, leg_y + 8), 4)
                pygame.draw.line(surface, BLACK, (r.x + 30, leg_y), (r.x + 26, leg_y + 8), 4)

    def get_rect(self):
        y = self.pos_y if hasattr(self, "pos_y") else self.y
        # slightly smaller hitbox for fairness
        return pygame.Rect(self.x + 4, y + 4, self.width - 8, self.height - 8)


class Cactus:
    def __init__(self, x, speed):
        self.width = random.choice([15, 20, 30])
        self.height = random.choice([30, 40, 50])
        self.x = x
        self.y = GROUND_Y - self.height
        self.speed = speed

    def update(self):
        self.x -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (34, 120, 40),
                          (self.x, self.y, self.width, self.height), border_radius=3)

    def get_rect(self):
        return pygame.Rect(self.x + 2, self.y, self.width - 4, self.height)

    def off_screen(self):
        return self.x + self.width < 0


class Bird:
    """Flying obstacle that forces ducking."""
    def __init__(self, x, speed):
        self.width = 34
        self.height = 20
        self.x = x
        self.y = GROUND_Y - random.choice([40, 80, 110])
        self.speed = speed
        self.frame = 0
        self.timer = 0

    def update(self):
        self.x -= self.speed
        self.timer += 1
        if self.timer > 10:
            self.timer = 0
            self.frame = 1 - self.frame

    def draw(self, surface):
        wing_offset = -8 if self.frame == 0 else 8
        pygame.draw.ellipse(surface, (80, 80, 80), (self.x, self.y, self.width, self.height))
        pygame.draw.polygon(surface, (80, 80, 80), [
            (self.x + self.width // 2, self.y + self.height // 2),
            (self.x + self.width // 2 - 15, self.y + wing_offset),
            (self.x + self.width // 2 + 5, self.y + self.height // 2),
        ])

    def get_rect(self):
        return pygame.Rect(self.x + 4, self.y + 2, self.width - 8, self.height - 4)

    def off_screen(self):
        return self.x + self.width < 0


def draw_ground(surface, offset):
    pygame.draw.line(surface, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
    # dashed texture that scrolls
    dash_len = 20
    gap = 15
    total = dash_len + gap
    start = -int(offset) % total
    x = -total + start
    while x < WIDTH:
        pygame.draw.line(surface, GRAY, (x, GROUND_Y + 6), (x + dash_len, GROUND_Y + 6), 2)
        x += total


def draw_clouds(surface, clouds, offset):
    for cx, cy in clouds:
        x = (cx - offset * 0.3) % (WIDTH + 60) - 30
        pygame.draw.ellipse(surface, GRAY, (x, cy, 46, 16))
        pygame.draw.ellipse(surface, GRAY, (x + 15, cy - 6, 30, 16))


def game_over_screen(score, high_score):
    text = big_font.render("GAME OVER", True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    sub = font.render(f"Score: {score}   High Score: {high_score}", True, BLACK)
    screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 - 5))
    hint = font.render("Press R to restart or ESC to quit", True, BLACK)
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 25))


def main():
    dino = Dino()
    obstacles = []
    clouds = [(random.randint(0, WIDTH), random.randint(20, 100)) for _ in range(4)]

    speed = 7.0
    spawn_timer = 0
    spawn_interval = random.randint(60, 100)

    score = 0.0
    high_score = 0
    ground_offset = 0

    running = True
    game_active = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_SPACE, pygame.K_UP):
                    if game_active:
                        dino.jump()
                    else:
                        pass
                elif event.key == pygame.K_DOWN:
                    if game_active:
                        dino.duck(True)
                elif event.key == pygame.K_r:
                    if not game_active:
                        # reset
                        dino = Dino()
                        obstacles = []
                        speed = 7.0
                        spawn_timer = 0
                        spawn_interval = random.randint(60, 100)
                        score = 0.0
                        game_active = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dino.duck(False)

        screen.fill(WHITE)

        if game_active:
            dino.update()

            # spawn obstacles
            spawn_timer += 1
            if spawn_timer >= spawn_interval:
                spawn_timer = 0
                spawn_interval = random.randint(55, 110)
                if random.random() < 0.25 and score > 15:
                    obstacles.append(Bird(WIDTH + 20, speed))
                else:
                    obstacles.append(Cactus(WIDTH + 20, speed))

            for obs in obstacles:
                obs.speed = speed
                obs.update()
            obstacles = [o for o in obstacles if not o.off_screen()]

            # collision check
            dino_rect = dino.get_rect()
            for obs in obstacles:
                if dino_rect.colliderect(obs.get_rect()):
                    game_active = False
                    high_score = max(high_score, int(score))

            # scoring & speed ramp
            score += 0.1
            speed = 7.0 + score * 0.03
            ground_offset += speed

        # draw
        draw_clouds(screen, clouds, ground_offset)
        draw_ground(screen, ground_offset)
        dino.draw(screen)
        for obs in obstacles:
            obs.draw(screen)

        score_text = font.render(f"Score: {int(score)}", True, BLACK)
        screen.blit(score_text, (WIDTH - score_text.get_width() - 15, 15))

        if not game_active:
            game_over_screen(int(score), high_score)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()