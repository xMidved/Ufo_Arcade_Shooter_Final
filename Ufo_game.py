import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 800))
clock = pygame.time.Clock()


balls = []
gravity = 0.3
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
            self.vx = random.randint(-6,-3)

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
   fps = clock.tick(60)
   spawn_timer += fps
   screen.fill((30, 30, 30))


   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False


   # spawn every 3 seconds
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

   for ball in balls:
       ball[3] += gravity
       ball[0] += ball[2]
       ball[1] += ball[3]


       # bounce on floor
       if ball[1] > 785:
           ball[1] = 785
           ball[3] *= -1

              # bounce on left wall
        if ball[0] < 15:
            ball[0] = 15
            ball[2] *= -1

        # bounce on right wall
        if ball[0] > 585:
            ball[0] = 585
            ball[2] *= -1


       pygame.draw.circle(screen, (0, 200, 255),
                          (int(ball[0]), int(ball[1])), 15)


    pygame.display.flip()


pygame.quit()