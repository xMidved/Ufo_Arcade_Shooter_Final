import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Ball Blast Prototype")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 24)

# ------------------
# Cannon
# ------------------
player_width = 60
player_height = 20
player_x = 270
player_y = 750
player_speed = 20

# ------------------
# Bullets
# ------------------
bullets = []
bullet_speed = -25
fire_delay = 100
fire_timer = 0

# ------------------
# Balls
# ------------------
balls = []
gravity = 0.09
spawn_timer = 0
SPAWN_DELAY = 4000
MIN_RADIUS = 15

# ------------------
# Helpers
# ------------------
def spawn_ball(x, y, vx, vy, radius):
    hp = radius // 5
    balls.append([x, y, vx, vy, radius, hp])

# ------------------
# Game loop
# ------------------
running = True
while running:
    fps = clock.tick(60)
    fire_timer += fps
    spawn_timer += fps

    screen.fill((30, 30, 30))

    # ------------------
    # Events
    # ------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ------------------
    # Cannon movement
    # ------------------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    player_x = max(0, min(600 - player_width, player_x))
    cannon_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # ------------------
    # Auto fire
    # ------------------
    if fire_timer >= fire_delay:
        bullets.append([player_x + player_width // 2, player_y])
        fire_timer = 0

    # ------------------
    # Spawn balls (slower)
    # ------------------
    if spawn_timer > SPAWN_DELAY:
        side = random.choice(["left", "right"])
        y = random.randint(50, 200)
        radius = 40

        if side == "left":
            spawn_ball(15, y, 5, -5, radius)
        else:
            spawn_ball(585, y, -5, -5, radius)

        spawn_timer = 0

    # ------------------
    # Update balls
    # ------------------
    for ball in balls[:]:
        x, y, vx, vy, r, hp = ball

        vy += gravity
        x += vx
        y += vy

        # Floor
        if y > 800 - r:
            y = 800 - r
            vy *= -1

        # Walls
        if x < r:
            x = r
            vx *= -1
        if x > 600 - r:
            x = 600 - r
            vx *= -1

        ball[0], ball[1], ball[2], ball[3] = x, y, vx, vy

        ball_rect = pygame.Rect(x - r, y - r, r * 2, r * 2)

        if cannon_rect.colliderect(ball_rect):
            running = False

        # Draw ball
        pygame.draw.circle(screen, (0, 200, 255), (int(x), int(y)), r)

        # Draw HP text
        hp_text = font.render(str(hp), True, (255, 255, 255))
        screen.blit(hp_text, (x - hp_text.get_width() // 2, y - r - 18))

    # ------------------
    # Update bullets
    # ------------------
    for bullet in bullets[:]:
        bullet[1] += bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)
            continue

        bullet_rect = pygame.Rect(bullet[0] - 4, bullet[1] - 4, 8, 8)

        for ball in balls[:]:
            x, y, vx, vy, r, hp = ball
            ball_rect = pygame.Rect(x - r, y - r, r * 2, r * 2)

            if bullet_rect.colliderect(ball_rect):
                bullets.remove(bullet)
                ball[5] -= 1

                if ball[5] <= 0:
                    balls.remove(ball)
                    if r > MIN_RADIUS:
                        new_r = r // 2
                        spawn_ball(x, y, -abs(vx), -5, new_r)
                        spawn_ball(x, y, abs(vx), -5, new_r)
                break

        pygame.draw.circle(screen, (255, 255, 0),
                           (int(bullet[0]), int(bullet[1])), 4)

    # ------------------
    # Draw cannon
    # ------------------
    pygame.draw.rect(screen, (255, 100, 100), cannon_rect)

    pygame.display.flip()

pygame.quit()