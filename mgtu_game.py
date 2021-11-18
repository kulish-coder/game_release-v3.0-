 
import pygame
import random
from os import path
import json
#from db import db
from sql_bd import DateBaseSQL

db = DateBaseSQL()

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 480
HEIGHT = 600
FPS = 70

FONT_SIZE = 18

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("game by Kulishov")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, x, y, size=FONT_SIZE, color=WHITE):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def user_name(surf, text, x, y, size=FONT_SIZE):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        # super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10  # padding to bottom bording
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 6)
        self.speedx = random.randrange(-2, 2)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360

            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(heart, (25, 19))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



heart = pygame.image.load(path.join(img_dir, "heart.png")).convert()
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med1.png',
               'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
               'meteorBrown_tiny1.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
hearts = []
player = Player()
all_sprites.add(player)

for i in range(3):
    h = Heart(i * 30, HEIGHT - 20)
    all_sprites.add(h)
    hearts.append(h)

for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def update_game_screen(name: str, score: int):
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    draw_text(screen, str(score), WIDTH / 2, 10)
    user_name(screen, str(name), WIDTH / 3, 10)
    
    pygame.display.flip()


        


def run_game_loop(name: str):
    amount_of_life = 3
    running, score = True, 0
    while amount_of_life > 0 and running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()

        hits = pygame.sprite.groupcollide (mobs, bullets, True, True)
        for hit in hits:
            score += 50 - hit.radius
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)

        collision = pygame.sprite.spritecollide(player, mobs, False,
                                                   pygame.sprite.collide_circle,)


        if collision:
            collision[0].kill()
            amount_of_life = amount_of_life - 1
            hearts.pop(-1).kill()


        update_game_screen(name=name, score=score)

    db.set(name, score)
    return score


def init_score_screen():
    name, score = '', 0
    is_run = True
    while is_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_run = False
            elif event.type == pygame.KEYDOWN:
                if event.key in {pygame.K_ESCAPE, pygame.K_RETURN}:
                    is_run = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode


        screen.fill(BLACK)
        draw_text(screen, 'Введите имя:', WIDTH // 2, HEIGHT // 2)
        draw_text(screen, name, WIDTH // 2, HEIGHT // 2 + 20)
        pygame.display.flip()

    score = run_game_loop(name=name)

    return name


name = init_score_screen()

def score_game():
    return(f'Your score is: {db.get(name)}')

def top_gamers():
    offset = 0 
    for u_name, u_score in db.get():
        draw_text(screen, (f'{u_name}: {u_score}'), WIDTH // 2, HEIGHT - 150 - offset)
        offset -= 30

game_over_loop = True
while game_over_loop:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_loop = False
            elif event.type == pygame.KEYDOWN:
                if event.key in {pygame.K_ESCAPE, pygame.K_RETURN}:
                    game_over_loop = False


        screen.fill(BLACK)
        draw_text(screen, 'Game Over', WIDTH // 2, HEIGHT - 450)
        draw_text(screen, score_game(), WIDTH // 2, HEIGHT // 2)
        draw_text(screen, 'Best scores:', WIDTH // 2, HEIGHT - 200)
        top_gamers()  
        pygame.display.flip()



pygame.quit()

print('Game Over')

