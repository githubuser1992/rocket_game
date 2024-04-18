# https://realpython.com/pygame-a-primer/#note-on-sources

import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_UP, 
    K_DOWN, 
    K_LEFT, 
    K_RIGHT, 
    K_ESCAPE, 
    KEYDOWN, 
    QUIT
)
pygame.init()
# setup drawing
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


image_rocket = pygame.image.load("assets/rocket.png")
img_rocket = pygame.transform.scale(image_rocket, (300, 300)).convert()

image_pineapple = pygame.image.load("assets/pineapple.png")
img_pineapple = pygame.transform.scale(image_pineapple, (300, 300)).convert()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = img_rocket
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()
    
    def update(self, pressed_keys):
        # key press 
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        # boundaries check
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
player = Player()
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = img_pineapple
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# run until the user quits
running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                runnign = False
        elif event.type == QUIT: # handles when the window is closed
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)


    screen.fill((0,0,0)) # paint background
    
    player.update(pygame.key.get_pressed())
    enemies.update()
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    if pygame.sprite.spritecollideany(player, enemies):
        # player.kill()
        # running = False
        print("collide")
    pygame.display.flip() # dump everything on the screen

# loop exited, quit now
pygame.quit()