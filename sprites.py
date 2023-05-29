import random
import pygame
from config import WIDTH, HEIGHT, WIDTH_CARRO, HEIGHT_CARRO, WIDTH_NPC, HEIGHT_NPC, WIDTH_PISTA, HEIGHT_PISTA
from assets import CARRO_IMG,  PISTA_IMG, NPC_IMG, EXPLOSION_ANIM
#from game_screen import Pontuacao 

posicoesx_iniciais = [175, 225, 275, 325]
posicoesy_iniciais = [0, -100, -200, -300, -400, -500, -600, -700, -800, -900]

class Pista(pygame.sprite.Sprite):
    def __init__(self, groups, assets):

        pygame.sprite.Sprite.__init__(self)

        self.image = assets['pista']
        #self.mask = pygame.mask.from_surface(self.image)
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
        #self.mask = pygame.mask.from_surface(self.image)
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
        #self.mask = pygame.mask.from_surface(self.image)
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


class Explosion(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, center, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Armazena a animação de explosão
        self.explosion_anim = assets['explosion_anim']

        # Inicia o processo de animação colocando a primeira imagem na tela.
        self.frame = 0  # Armazena o índice atual na animação
        self.image = self.explosion_anim[self.frame]
        self.mask = pygame.mask.from_surface(self.image)  # Pega a primeira imagem
        self.rect = self.image.get_rect()
        self.rect.center = center  # Posiciona o centro da imagem

        # Guarda o tick da primeira imagem, ou seja, o momento em que a imagem foi mostrada
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        # Quando pygame.time.get_ticks() - self.last_update > self.frame_ticks a
        # próxima imagem da animação será mostrada
        self.frame_ticks = 50

    def update(self):
        # Verifica o tick atual.
        now = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:
            # Marca o tick da nova imagem.
            self.last_update = now

            # Avança um quadro.
            self.frame += 1

            # Verifica se já chegou no final da animação.
            if self.frame == len(self.explosion_anim):
                # Se sim, tchau explosão!
                self.kill()
            else:
                # Se ainda não chegou ao fim da explosão, troca de imagem.
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center