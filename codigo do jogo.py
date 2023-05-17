# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random

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
paisagem_img = pygame.image.load('Paisagem2..png').convert_alpha()
pista_img = pygame.image.load('Mini pista.png').convert_alpha()
carro_img = pygame.image.load('obstaculo 1.png').convert_alpha()
carro_img = pygame.transform.scale(carro_img, (35, 50))
npc_img = pygame.image.load('obstaculo 2.png').convert_alpha()
npc_img = pygame.transform.scale(npc_img, (35, 50))

posicoes_iniciais = [175, 225, 275, 325]

class Pista(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.speedx = 0
        self.speedy = 4

    def update(self):
        # Atualizando a posição do meteoro
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Se o meteoro passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.y > HEIGHT:
            self.rect.y = -40

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
        if self.rect.top < HEIGHT/2:
            self.rect.top = HEIGHT/2

class NPC(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.speedx = 0
        self.speedy = 3
        self.rect.centerx = posicoes_iniciais[random.randint(0,3)]
        self.rect.bottom = random.randint(-600, 0)

    def update(self):
        # Atualização da posição da nave
        self.rect.x += self.speedx
        self.rect.y += self.speedy 

        # Mantem dentro da tela
        if self.rect.y > HEIGHT:
            self.rect.centerx = posicoes_iniciais[random.randint(0,3)]
            self.rect.bottom = random.randint(-600, 0)

all_sprites = pygame.sprite.Group()
all_pistas = pygame.sprite.Group()
all_npcs = pygame.sprite.Group()

for i in range(16):
    pista = Pista(pista_img)
    pista.rect.y = 40 * i 
    all_pistas.add(pista)
    all_sprites.add(pista)

for l in range(10):
    npc = NPC(npc_img)
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

        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                carro.speedx += 4
            if event.key == pygame.K_RIGHT:
                carro.speedx -= 4
            if event.key == pygame.K_UP:
                carro.speedy += 8


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