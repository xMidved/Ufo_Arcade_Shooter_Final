import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 830))
pygame.display.set_caption("Ufo Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

MIN_RADIUS = 25
FIELD_WIDTH = 800
FLOOR_Y = 800

# Load images
bullet_img = pygame.image.load("assets/Bullet.png").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (18, 18))
neptune_img = pygame.image.load("assets/neptune.png").convert_alpha()
neptune_img = pygame.transform.scale(neptune_img, (450, 450))
earth_img = pygame.image.load("assets/earth.png").convert_alpha()
earth_img = pygame.transform.scale(earth_img, (200, 200))
ufo_img_orig = pygame.image.load("assets/UFO.png").convert_alpha()
ufo_img_orig = pygame.transform.scale(ufo_img_orig, (100, 100))
meteor_img = pygame.image.load("assets/meteor.png").convert_alpha()
wave_sheet = pygame.image.load("assets/wave sprite.png").convert_alpha()
wave_frames = []
frame_width = wave_sheet.get_width() // 16   # adjust if not 8 frames
frame_height = wave_sheet.get_height()

for i in range(16):
    frame = wave_sheet.subsurface(
        (i * frame_width, 0, frame_width, frame_height)
    )
    wave_frames.append(frame)
wave_frame_index = 0
wave_anim_timer = 0
wave_anim_speed = 100   # lower = faster animation

# PLAYER
player_speed = 10
player_width = 50
player_height = 27
ufo_width = ufo_img_orig.get_width()
ufo_height = ufo_img_orig.get_height()

# BULLETS
BULLET_SPEED = 15
fire_delay = 150

# PLANETS
PLANET_INTERVAL = 15000  # spawn every 15 sec

# POWER UPS
POWER_TYPES = ["rapid_fire", "double_shot", "triple_shot"]
POWER_DURATION = 5000

gravity = 0.2


# BALL CLASS
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
        surface.blit(self.image, (int(self.x - self.r), int(self.y - self.r)))
        hp_text = font.render(str(self.hp), True, (255, 255, 255))
        surface.blit(
            hp_text,
            (int(self.x - hp_text.get_width() // 2),
             int(self.y - hp_text.get_height() // 2))
        )

    def get_rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)


# POWERUP CLASS
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


# RESET FUNCTION
def reset_game():
    global player_x, bullets, balls, powerups, active_power, power_timer
    global planet_active, planet_hp, planet_timer, planet_spawn_timer, wind_force, wave_timer
    global score, fire_timer, spawn_timer, fire_delay

    player_x = FIELD_WIDTH // 2 - player_width // 2
    bullets = []
    balls = []
    powerups = []
    active_power = None
    power_timer = 0
    planet_active = None
    planet_hp = 0
    planet_timer = 0
    planet_spawn_timer = 0
    wind_force = 0
    wave_timer = 0
    score = 0
    fire_timer = 0
    spawn_timer = 0
    fire_delay = 150


# END SCREEN FUNCTION
def end_screen(final_score):
    button_rect = pygame.Rect(FIELD_WIDTH//2 - 100, 600, 200, 50)
    while True:
        screen.fill((0, 0, 0))
        title_text = font.render("You Died!", True, (255, 0, 0))
        screen.blit(title_text, (FIELD_WIDTH//2 - title_text.get_width()//2, 400))
        score_text = font.render(f"Score: {final_score}", True, (255, 255, 255))
        screen.blit(score_text, (FIELD_WIDTH//2 - score_text.get_width()//2, 450))
        pygame.draw.rect(screen, (0, 200, 0), button_rect)
        btn_text = font.render("Restart", True, (255, 255, 255))
        screen.blit(btn_text, (button_rect.x + button_rect.width//2 - btn_text.get_width()//2,
                               button_rect.y + button_rect.height//2 - btn_text.get_height()//2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True
        pygame.display.flip()
        clock.tick(60)


# INITIAL RESET
reset_game()
running = True

# MAIN LOOP
while True:
    dt = clock.tick(60)
    fire_timer += dt
    spawn_timer += dt
    planet_spawn_timer += dt

    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    player_x = max(0, min(FIELD_WIDTH - ufo_width, player_x))
    cannon_rect = pygame.Rect(player_x + 25, 720 + 30, player_width, player_height)
    pygame.draw.rect(screen, (255, 0, 0), cannon_rect, 2)
    ufo_img = ufo_img_orig

    # POWER TIMER
    if active_power:
        power_timer += dt
        if power_timer >= POWER_DURATION:
            active_power = None
            fire_delay = 150
    if active_power == "rapid_fire":
        fire_delay = 60

    # PLANETS
    planet_rect = pygame.Rect(FIELD_WIDTH//2 - 80, 80, 160, 160)
    if planet_active:
        planet_timer += dt
        if planet_active == "neptune":
            screen.blit(neptune_img, (planet_rect.x - 150, planet_rect.y - 150))
            if (planet_timer // 2000) % 2 == 0:
                wind_force = 3
            else:
                wind_force = -3
            player_x += wind_force
        elif planet_active == "earth":
            screen.blit(earth_img, (planet_rect.x-20, planet_rect.y-20))

            wave_timer += dt

    # When wave attack is active
            if wave_timer > 2500:

                # Animate waves
                wave_anim_timer += dt
                if wave_anim_timer > wave_anim_speed:
                    wave_frame_index = (wave_frame_index + 1) % len(wave_frames)
                    wave_anim_timer = 0

                current_wave = wave_frames[wave_frame_index]

                # Scale wave to match hitbox
                scaled_wave = pygame.transform.scale(current_wave, (250, 150))

        # Draw waves
                screen.blit(scaled_wave, (0, FLOOR_Y - 150))
                screen.blit(scaled_wave, (FIELD_WIDTH - 250, FLOOR_Y - 150))

            # Invisible hitboxes
                left_wave = pygame.Rect(0, FLOOR_Y - 150, 250, 150)
                right_wave = pygame.Rect(FIELD_WIDTH - 250, FLOOR_Y - 150, 250, 150)

                # Only hit on 8th frame
                if wave_frame_index == 7 or wave_frame_index == 8 or wave_frame_index == 9:
                    if cannon_rect.colliderect(left_wave) or cannon_rect.colliderect(right_wave):
                        if end_screen(score):
                            reset_game()
                        else:
                            pygame.quit()
                            exit()

        # Reset after attack duration
                if wave_timer > 4000:
                    wave_timer = 0
        # Planet HP Bar
        pygame.draw.rect(screen, (100, 0, 0), (250, 40, 300, 20))
        pygame.draw.rect(screen, (255, 0, 0), (250, 40, 300 * (planet_hp/40), 20))
        if planet_hp <= 0:
            planet_spawn_timer = 0
            planet_active = None
            wind_force = 0
            wave_timer = 0
    else:
        if planet_spawn_timer >= PLANET_INTERVAL:
            planet_active = random.choice(["neptune", "earth"])
            planet_hp = 40
            planet_timer = 0
            planet_spawn_timer = 0

    # AUTO FIRE
    if fire_timer >= fire_delay:
        cx = player_x + 50
        cy = 720 + 25
        if active_power == "double_shot":
            bullets.append([cx - 15, cy, 0, -BULLET_SPEED])
            bullets.append([cx + 15, cy, 0, -BULLET_SPEED])
        elif active_power == "triple_shot":
            bullets.append([cx, cy, 0, -BULLET_SPEED])
            bullets.append([cx, cy, -5, -BULLET_SPEED])
            bullets.append([cx, cy, 5, -BULLET_SPEED])
        else:
            bullets.append([cx, cy, 0, -BULLET_SPEED])
        fire_timer = 0

    # SPAWN BALLS
    if spawn_timer > 5000:
        balls.append(Ball())
        spawn_timer = 0

    # BALLS
    for ball in balls[:]:
        ball.update()
        if cannon_rect.colliderect(ball.get_rect()):
            if end_screen(score):
                reset_game()
            else:
                pygame.quit()
                exit()
        ball.draw(screen)

    # BULLETS
    for bullet in bullets[:]:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]
        if bullet[1] < 0 or bullet[0] < 0 or bullet[0] > FIELD_WIDTH:
            bullets.remove(bullet)
            continue
        bullet_rect = pygame.Rect(bullet[0] - 5, bullet[1] - 5, 10, 10)
        # Bullet hits planet
        if planet_active and bullet_rect.colliderect(planet_rect):
            bullets.remove(bullet)
            planet_hp -= 1
            continue
        # Bullet hits ball
        for ball in balls[:]:
            if bullet_rect.colliderect(ball.get_rect()):
                bullets.remove(bullet)
                ball.take_damage()
                score += 1
                if ball.hp <= 0:
                    score += 10
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

    # POWERUPS
    for p in powerups[:]:
        p.update()
        p.draw(screen)
        if cannon_rect.colliderect(p.get_rect()):
            active_power = p.kind
            power_timer = 0
            powerups.remove(p)
        elif p.y > 1000:
            powerups.remove(p)

    # SCORE
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    # PLAYER
    screen.blit(ufo_img, (player_x, 720))
    pygame.display.flip()
