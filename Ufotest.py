import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Ball Blast Prototype")
clock = pygame.time.Clock()

# ------------------
# Cannon
# ------------------
player_width = 60
player_height = 20
player_x = 270
player_y = 750
player_speed = 6

# ------------------
# Bullets
# ------------------
bullets = []
bullet_speed = -10
fire_delay = 200   # ms
fire_timer = 0

# ------------------
# Falling balls
# ------------------
balls = []
gravity = 0.3
spawn_timer = 0

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

    # ------------------
    # Auto fire
    # ------------------
    if fire_timer >= fire_delay:
        bullets.append([player_x + player_width // 2, player_y])
        fire_timer = 0

    # ------------------
    # Spawn falling balls
    # ------------------
    if spawn_timer > 3000:
        side = random.choice(["left", "right"])
        if side == "left":
            balls.append([15, random.randint(50, 200), 5, -5])
        else:
            balls.append([585, random.randint(50, 200), -5, -5])
        spawn_timer = 0

    # ------------------
    # Cannon rect
    # ------------------
    cannon_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # ------------------
    # Update balls
    # ------------------
    for ball in balls[:]:
        ball[3] += gravity
        ball[0] += ball[2]
        ball[1] += ball[3]

        # floor bounce
        if ball[1] > 785:
            ball[1] = 785
            ball[3] *= -1

        # wall bounce
        if ball[0] < 15:
            ball[0] = 15
            ball[2] *= -1
        if ball[0] > 585:
            ball[0] = 585
            ball[2] *= -1

        ball_rect = pygame.Rect(ball[0] - 15, ball[1] - 15, 30, 30)

        # Ball hits cannon = death
        if cannon_rect.colliderect(ball_rect):
            running = False

        pygame.draw.circle(
            screen, (0, 200, 255),
            (int(ball[0]), int(ball[1])), 15
        )

    # ------------------
    # Update bullets
    # ------------------
    for bullet in bullets[:]:
        bullet[1] += bullet_speed

        if bullet[1] < 0:
            bullets.remove(bullet)
            continue

        bullet_rect = pygame.Rect(bullet[0] - 5, bullet[1] - 5, 10, 10)

        for ball in balls[:]:
            ball_rect = pygame.Rect(ball[0] - 15, ball[1] - 15, 30, 30)
            if bullet_rect.colliderect(ball_rect):
                bullets.remove(bullet)
                balls.remove(ball)
                break

        pygame.draw.circle(
            screen, (255, 255, 0),
            (int(bullet[0]), int(bullet[1])), 5
        )

    # ------------------
    # Draw cannon
    # ------------------
    pygame.draw.rect(
        screen, (255, 100, 100),
        cannon_rect
    )

    pygame.display.flip()

pygame.quit()