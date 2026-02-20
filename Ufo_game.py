import pygame
import random


pygame.init()
screen = pygame.display.set_mode((600, 800))
clock = pygame.time.Clock()


balls = []
gravity = 0.3
spawn_timer = 0


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
           balls.append([15, random.randint(50, 200), 6, -5])
       else:
           balls.append([585, random.randint(50, 200), -6, -5])


       spawn_timer = 0


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
