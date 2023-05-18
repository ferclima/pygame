# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
import numpy as np

pygame.init()

# ----- Gera tela principal
WIDTH = 500
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Carros 5')

# ----- Inicia estruturas de dados
clock = pygame.time.Clock()
FPS = 30
game = True
WIDTH_CARRO = 27
HEIGHT_CARRO = 50
WIDTH_NPC = 35
HEIGHT_NPC = 50
WIDTH_PISTA = 208
HEIGHT_PISTA = 40
paisagem_img = pygame.image.load('Paisagem2..png').convert_alpha()
pista_img = pygame.image.load('Mini pista.png').convert_alpha()
carro_img = pygame.image.load('carrinho2-removebg-preview.png').convert_alpha()
carro_img = pygame.transform.scale(carro_img, (WIDTH_CARRO, HEIGHT_CARRO))

npc_img1 = pygame.image.load('obstaculo 1.png').convert_alpha()
npc_img1 = pygame.transform.scale(npc_img1, (WIDTH_NPC, HEIGHT_CARRO))
npc_img2 = pygame.image.load('obstaculo 2.png').convert_alpha()
npc_img2 = pygame.transform.scale(npc_img2, (WIDTH_NPC, HEIGHT_NPC))
npc_img3 = pygame.image.load('obstaculo 3.png').convert_alpha()
npc_img3 = pygame.transform.scale(npc_img3, (WIDTH_NPC, HEIGHT_NPC))
npc_img4 = pygame.image.load('obstaculo 4.png').convert_alpha()
npc_img4 = pygame.transform.scale(npc_img4, (WIDTH_NPC, HEIGHT_NPC))

lista_img_npcs = [npc_img1, npc_img2, npc_img3, npc_img4]

posicoesx_iniciais = [175, 225, 275, 325]
posicoesy_iniciais = np.arange(-900, 0, 100)

class Pista(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.speedx = 0
        self.speedy = 8

    def update(self):
        # Atualizando a posição do meteoro
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Se o meteoro passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.y > HEIGHT:
            self.rect.y = -39

class Carro(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.speedx = 0
        self.speedy = 4
        self.rect.centerx = WIDTH /2
        self.rect.bottom = HEIGHT - 100

    def update(self):
        # Atualização da posição da nave
        self.rect.x += self.speedx
        self.rect.y += self.speedy 

        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 200:
            self.rect.top = 200

class NPC(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.speedx = 0
        self.speedy = 3
        self.rect.centerx = posicoesx_iniciais[random.randint(0,3)]
        self.rect.bottom = posicoesy_iniciais[random.randint(0,((len(posicoesy_iniciais))-1))]

    def update(self):
        # Atualização da posição da nave
        self.rect.x += self.speedx
        self.rect.y += self.speedy 

        # Mantem dentro da tela
        if self.rect.y > HEIGHT:
            self.rect.centerx = posicoesx_iniciais[random.randint(0,3)]
            self.rect.bottom = posicoesy_iniciais[random.randint(0,((len(posicoesy_iniciais))-1))]

all_sprites = pygame.sprite.Group()
all_pistas = pygame.sprite.Group()
all_npcs = pygame.sprite.Group()

for i in range(16):
    pista = Pista(pista_img)
    pista.rect.y = 40 * i 
    all_pistas.add(pista)
    all_sprites.add(pista)

for l in range(10):
    npc = NPC(lista_img_npcs[random.randint(0,3)])
    all_npcs.add(npc)
    all_sprites.add(npc)

carro = Carro(carro_img)
all_sprites.add(carro)

# ===== Loop principal =====
while game:
    clock.tick(FPS)

    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False
        # Verifica se apertou alguma tecla.
        if event.type == pygame.KEYDOWN:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                carro.speedx -= 4
            if event.key == pygame.K_RIGHT:
                carro.speedx += 4
            if event.key == pygame.K_UP:
                carro.speedy -= 8
            if event.key == pygame.K_DOWN:
                carro.speedy += 4

        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                carro.speedx += 4
            if event.key == pygame.K_RIGHT:
                carro.speedx -= 4
            if event.key == pygame.K_UP:
                carro.speedy += 8
            if event.key == pygame.K_DOWN:
                carro.speedy -= 4

    hits = pygame.sprite.spritecollide(carro, all_npcs, True)

    if carro.rect.centerx > 354 or carro.rect.centerx < 146:
        game = False 
    
    if len(hits) > 0:
        game = False 

    all_pistas.update()
    all_npcs.update()
    all_sprites.update()

    # ----- Gera saídas

    window.fill((150, 0, 0))  # Preenche com a cor branca
    window.blit(paisagem_img, (0, 0))
    
    all_sprites.draw(window)

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados