import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 1000))
pygame.display.set_caption("Ufo Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

MIN_RADIUS = 25
FIELD_WIDTH = 800
FLOOR_Y = 800

bullet_img = pygame.image.load("assets/Bullet.png").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (18, 18))

ufo_img = pygame.image.load("assets/UFO.png").convert_alpha()
ufo_img = pygame.transform.scale(ufo_img, (100, 100))

meteor_img = pygame.image.load("assets/meteor.png").convert_alpha()

# ---------------- PLAYER ----------------
player_width = 50
player_height = 20
player_x = FIELD_WIDTH // 2 - player_width // 2
player_y = 720
player_speed = 10

# ---------------- BULLETS ----------------
bullets = []  # [x, y, vx, vy]
BULLET_SPEED = 15
fire_delay = 150
fire_timer = 0

# ---------------- GAME ----------------
gravity = 0.2
balls = []
spawn_timer = 0
score = 0

# ---------------- POWER UPS ----------------
POWER_TYPES = ["rapid_fire", "double_shot", "triple_shot"]
powerups = []
active_power = None
power_timer = 0
POWER_DURATION = 5000


# ---------------- BALL ----------------
class Ball:
    def __init__(self, x=None, y=None, vx=None, vy=None, radius=None):
        self.r = radius if radius else random.randint(20, 40)
        self.hp = self.r // 5

        self.image = pygame.transform.scale(
            meteor_img, (self.r * 2, self.r * 2)
        )

        if x is None:
            side = random.choice(["left", "right"])
            self.y = random.randint(50, 200)
            self.vy = -5
            if side == "left":
                self.x = self.r
                self.vx = random.randint(3, 6)
            else:
                self.x = FIELD_WIDTH - self.r
                self.vx = random.randint(-6, -3)
        else:
            self.x, self.y, self.vx, self.vy = x, y, vx, vy

    def update(self):
        self.vy += gravity
        self.x += self.vx
        self.y += self.vy

        if self.y > FLOOR_Y - self.r:
            self.y = FLOOR_Y - self.r
            self.vy = -self.vy + gravity

        if self.x < self.r:
            self.x = self.r
            self.vx = -self.vx
        if self.x > FIELD_WIDTH - self.r:
            self.x = FIELD_WIDTH - self.r
            self.vx = -self.vx

    def take_damage(self):
        self.hp -= 1

    def draw(self, surface):
        surface.blit(
            self.image,
            (int(self.x - self.r), int(self.y - self.r))
        )
        hp_text = font.render(str(self.hp), True, (255, 255, 255))
        surface.blit(
            hp_text,
            (int(self.x - hp_text.get_width() // 2),
             int(self.y - hp_text.get_height() // 2))
        )

    def get_rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)


# ---------------- POWERUP ----------------
class PowerUp:
    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind
        self.vy = 6
        self.size = 20
        self.color = {
            "rapid_fire": (255, 50, 50),
            "double_shot": (50, 255, 50),
            "triple_shot": (50, 50, 255)
        }[kind]

    def update(self):
        self.y += self.vy

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            (self.x - 10, self.y - 10, 20, 20)
        )

    def get_rect(self):
        return pygame.Rect(self.x - 10, self.y - 10, 20, 20)


# ---------------- MAIN LOOP ----------------
running = True
while running:
    dt = clock.tick(60)
    fire_timer += dt
    spawn_timer += dt

    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    player_x = max(0, min(FIELD_WIDTH - player_width, player_x))
    cannon_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # -------- POWER TIMER --------
    if active_power:
        power_timer += dt
        if power_timer >= POWER_DURATION:
            active_power = None
            fire_delay = 150

    if active_power == "rapid_fire":
        fire_delay = 60

    # -------- AUTO FIRE --------
    if fire_timer >= fire_delay:
        cx = player_x + player_width // 2

        if active_power == "double_shot":
            bullets.append([cx - 10, player_y, 0, -BULLET_SPEED])
            bullets.append([cx + 10, player_y, 0, -BULLET_SPEED])

        elif active_power == "triple_shot":
            bullets.append([cx, player_y, 0, -BULLET_SPEED])
            bullets.append([cx, player_y, -5, -BULLET_SPEED])
            bullets.append([cx, player_y, 5, -BULLET_SPEED])

        else:
            bullets.append([cx, player_y, 0, -BULLET_SPEED])

        fire_timer = 0

    # -------- SPAWN BALLS --------
    if spawn_timer > 5000:
        balls.append(Ball())
        spawn_timer = 0

    # -------- BALLS --------
    for ball in balls[:]:
        ball.update()
        if cannon_rect.colliderect(ball.get_rect()):
            running = False
        ball.draw(screen)

    # -------- BULLETS --------
    for bullet in bullets[:]:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]

        if bullet[1] < 0 or bullet[0] < 0 or bullet[0] > FIELD_WIDTH:
            bullets.remove(bullet)
            continue

        bullet_rect = pygame.Rect(bullet[0] - 5, bullet[1] - 5, 10, 10)

        for ball in balls[:]:
            if bullet_rect.colliderect(ball.get_rect()):
                bullets.remove(bullet)
                ball.take_damage()
                score += 1  # hit score

                if ball.hp <= 0:
                    score += 10  # destroy bonus
                    x, y, vx, r, vy = ball.x, ball.y, ball.vx, ball.r, ball.vy
                    balls.remove(ball)

                    if random.random() < 0.3:
                        powerups.append(PowerUp(x, y, random.choice(POWER_TYPES)))

                    if r > MIN_RADIUS:
                        new_r = r // 1.5
                        split_vy = -abs(vy)
                        balls.append(Ball(x, y, -abs(vx), split_vy, new_r))
                        balls.append(Ball(x, y, abs(vx), split_vy, new_r))
                break

        screen.blit(bullet_img, (bullet[0] - 9, bullet[1] - 9))

    # -------- POWERUPS --------
    for p in powerups[:]:
        p.update()
        p.draw(screen)
        if cannon_rect.colliderect(p.get_rect()):
            active_power = p.kind
            power_timer = 0
            powerups.remove(p)
        elif p.y > 1000:
            powerups.remove(p)

    # -------- SCORE --------
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    screen.blit(ufo_img, (player_x, player_y))
    pygame.display.flip()

pygame.quit()