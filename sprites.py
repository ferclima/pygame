import random
import pygame
from config import WIDTH, HEIGHT, WIDTH_CARRO, HEIGHT_CARRO, WIDTH_NPC, HEIGHT_NPC, WIDTH_PISTA, HEIGHT_PISTA
from assets import CARRO_IMG,  PISTA_IMG, NPC_IMG, EXPLOSION_ANIM

posicoesx_iniciais = [175, 225, 275, 325]
posicoesy_iniciais = [0, -100, -200, -300, -400, -500, -600, -700, -800, -900]

class Pista(pygame.sprite.Sprite):
    def __init__(self, groups, assets):

        pygame.sprite.Sprite.__init__(self)
        self.image = assets['pista']
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.speedx = 0
        self.speedy = 8
        self.groups = groups
        self.assets = assets

    def update(self):

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.y > HEIGHT:
            self.rect.y = -39

class Carro(pygame.sprite.Sprite):
    def __init__(self, groups, assets):

        pygame.sprite.Sprite.__init__(self)
        self.image = assets['carro']
        self.rect = self.image.get_rect()
        self.speedx = 0
        self.speedy = 4
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-100
        self.groups = groups
        self.assets = assets

    def update(self):

        self.rect.x += self.speedx
        self.rect.y += self.speedy 
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 200:
            self.rect.top = 200

class NPC(pygame.sprite.Sprite):
    def __init__(self, groups, assets, ID):

        pygame.sprite.Sprite.__init__(self)
        self.image = assets['NPCs'][random.randint(0,3)]
        self.rect = self.image.get_rect()
        self.speedx = 0
        self.speedy = random.randint(1,4)
        self.rect.centerx = posicoesx_iniciais[random.randint(0,3)]
        self.rect.bottom = posicoesy_iniciais[random.randint(0,9)]
        self.groups = groups
        self.assets = assets
        self.ID = ID

    def update(self):

        self.rect.x += self.speedx
        self.rect.y += self.speedy 
        if self.rect.y > HEIGHT:
            self.rect.centerx = posicoesx_iniciais[random.randint(0,3)]
            self.rect.bottom = posicoesy_iniciais[random.randint(0,9)]
            self.speedy = random.randint(1,4)

class Fundo(pygame.sprite.Sprite):
    def __init__(self, groups, assets):

        pygame.sprite.Sprite.__init__(self)
        self.image = assets['paisagem'][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.speedx = 0
        self.speedy = 14
        self.groups = groups
        self.assets = assets
        self.pontuacao = 0

    def update(self):

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.y > (2*HEIGHT):
            self.rect.y = -HEIGHT
        if self.pontuacao > 2000 and self.pontuacao < 3000:
            self.image = self.assets['paisagem'][1]
        elif self.pontuacao > 3000 and self.pontuacao < 4000:
            self.image = self.assets['paisagem'][2]
        elif self.pontuacao > 4000 and self.pontuacao < 5000:
            self.image = self.assets['paisagem'][3]
        elif self.pontuacao > 5000:
            self.image = self.assets['paisagem'][4]

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, assets):

        pygame.sprite.Sprite.__init__(self)
        self.explosion_anim = assets['explosion_anim']
        self.frame = 0
        self.image = self.explosion_anim[self.frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = 50
    def update(self):

        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_update
        if elapsed_ticks > self.frame_ticks:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center