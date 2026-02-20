import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 800))
clock = pygame.time.Clock()

gravity = 0.3
balls = []
spawn_timer = 0

class Ball:
    def __init__(self):
        self.r = random.randint(10, 40)                  # fixed radius
        self.color = (0, 200, 255)                        # fixed color
        self.y = random.randint(50, 200)
        self.vy = -5

        side = random.choice(["left", "right"])
        if side == "left":
            self.x = self.r
            self.vx = 5
        else:
            self.x = 600 - self.r
            self.vx = -5

    def update(self):
        self.vy += gravity
        self.x += self.vx
        self.y += self.vy

        # bounce on floor
        if self.y > 800 - self.r:
            self.y = 800 - self.r
            self.vy *= -1

        # bounce on walls
        if self.x < self.r:
            self.x = self.r
            self.vx *= -1
        if self.x > 600 - self.r:
            self.x = 600 - self.r
            self.vx *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.r)


running = True
while running:
    dt = clock.tick(60)
    spawn_timer += dt
    screen.fill((30, 30, 30))   # clear screen every frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # spawn ball every 3 seconds
    if spawn_timer > 3000:
        balls.append(Ball())
        spawn_timer = 0

    # update and draw all balls
    for ball in balls:
        ball.update()
        ball.draw(screen)

    pygame.display.flip()

pygame.quit()
