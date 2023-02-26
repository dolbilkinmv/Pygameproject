import pygame
import random

# Константы
WIDTH = 600
HEIGHT = 700
FPS = 60
gameover = False
PAUSE = False
coins = 0
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hit the Island")
clock = pygame.time.Clock()
score = 0


# Создаем игровые объекты
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:\\Users\\92552\\Downloads\\pythonProject2\\ps.png")
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Circle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("circle.png")
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 450
        self.speedy = random.randrange(-8, 8)
        while self.speedy == 0:
            self.speedy = random.randrange(-8, 8)
        self.speedx = self.speedy * (1 + random.randrange(1, 4) / 10)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.x >= WIDTH - 50:
            self.speedx = -self.speedx
        elif self.rect.x <= 0:
            self.speedx = -self.speedx
        elif self.rect.y <= 0:
            self.speedy = -self.speedy


class Island(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ps.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = 40

    def update(self):
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)


score = 0
# Создаем спрайты
all_sprites = pygame.sprite.Group()
player = Player()
circle = Circle()
all_sprites.add(player)
all_sprites.add(circle)
islands = pygame.sprite.Group()
for i in range(1):
    island = Island()
    all_sprites.add(island)
    islands.add(island)
    islands.add(player)
mask1 = pygame.mask.from_surface(island.image)
mask2 = pygame.mask.from_surface(player.image)
mask3 = pygame.mask.from_surface(circle.image)
# Счетчик очков


# Цикл игры
font = pygame.font.Font(None, 48)
font1 = pygame.font.Font(None, 32)
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()
    keystate = pygame.key.get_pressed()
    if gameover == True:
        coins += score
        score = 0
        if keystate[pygame.K_r]:
            circle.rect.x = 350
            circle.rect.y = 450
            circle.speedy = random.randrange(-8, 8)
            circle.speedx = circle.speedy * (1 + random.randrange(1, 4) / 10)

            score = 0
            gameover = False
            PAUSE = False
    if keystate[pygame.K_ESCAPE]:
        if gameover == True:
            PAUSE = True

    # Проверяем столкновения
    hits = pygame.sprite.spritecollide(circle, islands, False)
    for hit in hits:
        if circle.rect.colliderect(hit.rect):
            if circle.rect.top < hit.rect.bottom and circle.speedy < 0:
                circle.rect.top = hit.rect.bottom
                circle.speedy = -circle.speedy * 1.05
            elif circle.rect.bottom > hit.rect.top and circle.speedy > 0:
                circle.rect.bottom = hit.rect.top
                circle.speedy = -circle.speedy * 1.05
            elif circle.rect.left < hit.rect.right and circle.speedx < 0:
                circle.rect.left = hit.rect.right
                circle.speedx = 0
            elif circle.rect.right > hit.rect.left and circle.speedx > 0:
                circle.rect.right = hit.rect.left
                circle.speedx = 0

    # Счетчик очков
    score += len(hits)
    score_surface = font1.render("Score: {}".format(score), True, WHITE)
    cois = font1.render("Coins: {}".format(coins), True, WHITE)

    # Рендеринг
    screen.fill(BLACK)
    if PAUSE:
        im1 = pygame.image.load("circle1.png")
        im2 = pygame.image.load("circle2.png")
        im3 = pygame.image.load("circle3.png")
        screen.blit(im1, (150, 100))
        screen.blit(font.render("15", True, WHITE), (150, 150))
        screen.blit(im2, (250, 100))
        screen.blit(font.render("30", True, WHITE), (250, 150))
        screen.blit(im3, (350, 100))
        screen.blit(font.render("50", True, WHITE), (350, 150))
        if keystate[pygame.K_1]:
            if coins > 15:
                circle.image = pygame.image.load("circle1.png")
                PAUSE = False
                coins -= 15
        if keystate[pygame.K_2]:
            if coins > 30:
                coins -= 30
                circle.image = pygame.image.load("circle2.png")
                PAUSE = False
        if keystate[pygame.K_3]:
            if coins > 50:
                coins -= 50
                circle.image = pygame.image.load("circle3.png")
                PAUSE = False
        if keystate[pygame.K_4]:
            circle.image = pygame.image.load("circle.png")
            PAUSE = False
    all_sprites.draw(screen)
    screen.blit(score_surface, (10, 6))
    screen.blit(cois, (10, 25))
    if circle.rect.y > HEIGHT + 50:
        score_surface = font.render("GAME OVER!", True, WHITE)
        gameover = True
        score_surface1 = font.render("Press 'R' to restart", True, WHITE)
        screen.blit(score_surface, (200, 300))
        screen.blit(score_surface1, (160, 335))
    pygame.display.flip()
    if circle.rect.y > HEIGHT + 50:
        gameover = True

print(score)
pygame.quit()
