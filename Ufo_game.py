import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

balls = []
gravity = 0.3

SPAWN_DELAY = 2000  
spawn_timer = 0

class Ball:
    def __init__(self):
        self.radius = 15
        self.x = random.randint(self.radius, 600 - self.radius)
        self.y = 0
        self.vy = 0

    def update(self):
        self.vy += gravity
        self.y += self.vy

        # bounce on floor
        if self.y + self.radius > 400:
            self.y = 400 - self.radius
            self.vy *= -0.8

    def draw(self):
        pygame.draw.circle(screen, (0, 200, 255), (int(self.x), int(self.y)), self.radius)

running = True
while running:
    dt = clock.tick(60)
    spawn_timer += dt
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # spawn ball every few seconds
    if spawn_timer > SPAWN_DELAY:
        balls.append(Ball())
        spawn_timer = 0

    for ball in balls:
        ball.update()
        ball.draw()

    pygame.display.flip()

pygame.quit()
