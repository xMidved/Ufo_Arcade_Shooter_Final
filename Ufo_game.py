import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Ufo Game")
clock = pygame.time.Clock()


# Player 
player_width = 60
player_height = 20
player_x = 270
player_y = 750
player_speed = 6

# Bullets
bullets = []
bullet_speed = -10
fire_delay = 200
fire_timer = 0

# Game Variables
gravity = 0.3
balls = []
spawn_timer = 0


# Ball Class
class Ball:
    def __init__(self):
        self.r = random.randint(15, 40)
        self.max_r = self.r
        self.color = (0, 200, 255)

        # Health based on size
        self.hp = self.r // 5   # Bigger ball = more HP

        self.y = random.randint(50, 200)
        self.vy = -5

        side = random.choice(["left", "right"])
        if side == "left":
            self.x = self.r
            self.vx = random.randint(3,6)
        else:
            self.x = 600 - self.r
            self.vx = random.randint(-3,-6)

    def update(self):
        self.vy += gravity
        self.x += self.vx
        self.y += self.vy

        # Floor bounce
        if self.y > 800 - self.r:
            self.y = 800 - self.r
            self.vy *= -1

        # Wall bounce
        if self.x < self.r:
            self.x = self.r
            self.vx *= -1
        if self.x > 600 - self.r:
            self.x = 600 - self.r
            self.vx *= -1

    def take_damage(self):
        self.hp -= 1

        # Shrink slightly when hit
        if self.r > 10:
            self.r -= 2

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.r)

    def get_rect(self):
        return pygame.Rect(
            self.x - self.r,
            self.y - self.r,
            self.r * 2,
            self.r * 2
        )


# Main Game Loop
running = True
while running:
    dt = clock.tick(60)
    fire_timer += dt
    spawn_timer += dt

    screen.fill((30, 30, 30))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    player_x = max(0, min(600 - player_width, player_x))
    cannon_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # Auto Fire
    if fire_timer >= fire_delay:
        bullets.append([player_x + player_width // 2, player_y])
        fire_timer = 0

    # Spawn Balls
    if spawn_timer > 3000:
        balls.append(Ball())
        spawn_timer = 0


    # Update Balls
    for ball in balls[:]:
        ball.update()

        # Collision with cannon
        if cannon_rect.colliderect(ball.get_rect()):
            running = False

        ball.draw(screen)

        # Update Bullets
    for bullet in bullets[:]:
        bullet[1] += bullet_speed

        if bullet[1] < 0:
            bullets.remove(bullet)
            continue

        bullet_rect = pygame.Rect(bullet[0] - 5, bullet[1] - 5, 10, 10)

        for ball in balls[:]:
            if bullet_rect.colliderect(ball.get_rect()):
                bullets.remove(bullet)
                ball.take_damage()

                if ball.hp <= 0:
                    balls.remove(ball)

                break   # stop checking other balls for this bullet

        # Draw bullet
        pygame.draw.circle(
            screen,
            (255, 255, 0),
            (int(bullet[0]), int(bullet[1])),
            5
        )


    # Draw Ufo
    pygame.draw.rect(screen, (255, 100, 100), cannon_rect)

    pygame.display.flip()

pygame.quit()

    pygame.display.flip()

pygame.quit()
