import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Ufo Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)
MIN_RADIUS = 25
bullet_img = pygame.image.load("Bullet.png").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (18, 18))  # resize if needed

# Player   
player_width = 60
player_height = 20
player_x = 270
player_y = 750
player_speed = 6

# Bullets
bullets = []
bullet_speed = -15
fire_delay = 150
fire_timer = 0

# Game Variables
gravity = 0.3
balls = []
spawn_timer = 0


# Ball Class
class Ball:
    def __init__(self, x=None, y=None, vx=None, vy=None, radius=None):
        if radius is None:
            self.r = random.randint(20, 40)
        else:
            self.r = radius

        self.color = (0, 200, 255)
        self.hp = self.r // 5

        if x is None:
            side = random.choice(["left", "right"])
            self.y = random.randint(50, 200)
            self.vy = -5

            if side == "left":
                self.x = self.r
                self.vx = random.randint(3, 6)
            else:
                self.x = 600 - self.r
                self.vx = random.randint(-6, -3)
        else:
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy

    def update(self):
        self.vy += gravity
        self.x += self.vx
        self.y += self.vy

        # Floor
        if self.y > 800 - self.r:
            self.y = 800 - self.r
            self.vy *= -1

        # Walls
        if self.x < self.r:
            self.x = self.r
            self.vx *= -1
        if self.x > 600 - self.r:
            self.x = 600 - self.r
            self.vx *= -1

    def take_damage(self):
        self.hp -= 1


    def draw(self, surface):
    # Draw ball
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.r)

    # Draw HP number
        hp_text = font.render(str(self.hp), True, (255, 255, 255))

        surface.blit(
    hp_text,
    (
        int(self.x - hp_text.get_width() // 2),
        int(self.y - hp_text.get_height() // 2)
    )
)
    def get_rect(self):
        return pygame.Rect(
            self.x - self.r,
            self.y - self.r,
            self.r * 2,
            self.r * 2
        )



    
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
                if bullet in bullets:
                    bullets.remove(bullet)

                ball.take_damage()

        # If ball destroyed
                if ball.hp <= 0:
                    x, y = ball.x, ball.y
                    vx = ball.vx
                    r = ball.r

                    balls.remove(ball)

            # Split if big enough
                    if r > MIN_RADIUS:
                        new_r = r // 1.5
                        balls.append(Ball(x, y, -abs(vx), -5, new_r))
                        balls.append(Ball(x, y, abs(vx), -5, new_r))

                break 
                
        # Draw bullet
        screen.blit(bullet_img,(int(bullet[0] - bullet_img.get_width() // 2),int(bullet[1] - bullet_img.get_height() // 2)))
    

    # Draw Ufo
    
    pygame.draw.rect(screen, (255, 100, 100), cannon_rect)

    pygame.display.flip()

pygame.quit()
