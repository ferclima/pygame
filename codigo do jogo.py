# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
import time

pygame.init()
pygame.mixer.init()

# ===== Loading dos sons do carro
pygame.mixer.music.load('Sons\carro-correndo-loop.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.load('Sons\carro-explosao.mp3')
carro_correndo = pygame.mixer.Sound('Sons\carro-correndo-loop.mp3')
carro_batida = pygame.mixer.Sound('Sons\carro-explosao.mp3')

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
WIDTH_NPC = 27
HEIGHT_NPC = 50
WIDTH_PISTA = 208
HEIGHT_PISTA = 40

assets = {}
paisagem_img = pygame.image.load('Imagens\Paisagem2..png').convert_alpha()
paisagem_img = pygame.transform.scale(paisagem_img, (WIDTH, HEIGHT))
pista_img = pygame.image.load('Imagens\Mini pista.png').convert_alpha()
carro_img = pygame.image.load('Imagens\carrinho2-removebg-preview.png').convert_alpha()
carro_img = pygame.transform.scale(carro_img, (WIDTH_CARRO, HEIGHT_CARRO))

Fonte = pygame.font.Font('fonte\PressStart2P.ttf', 25)

npc_img1 = pygame.image.load('Imagens\obstaculo 1.png').convert_alpha()
npc_img1 = pygame.transform.scale(npc_img1, (WIDTH_NPC, HEIGHT_CARRO))
npc_img2 = pygame.image.load('Imagens\obstaculo 2.png').convert_alpha()
npc_img2 = pygame.transform.scale(npc_img2, (WIDTH_NPC, HEIGHT_NPC))
npc_img3 = pygame.image.load('Imagens\obstaculo 3.png').convert_alpha()
npc_img3 = pygame.transform.scale(npc_img3, (WIDTH_NPC, HEIGHT_NPC))
npc_img4 = pygame.image.load('Imagens\obstaculo 4.png').convert_alpha()
npc_img4 = pygame.transform.scale(npc_img4, (WIDTH_NPC, HEIGHT_NPC))

lista_img_npcs = [npc_img1, npc_img2, npc_img3, npc_img4]

posicoesx_iniciais = [175, 225, 275, 325]
posicoesy_iniciais = [0, -100, -200, -300, -400, -500, -600, -700, -800, -900]

explosion_anim = []
for i in range(9):
    # Os arquivos de animação são numerados de 00 a 08
    filename = "Explosão\Explosion0{}.png".format(i)
    img = pygame.image.load(filename).convert_alpha()
    img = pygame.transform.scale(img, (32, 32))
    explosion_anim.append(img)
assets["explosion_anim"] = explosion_anim

class Pista(pygame.sprite.Sprite):
    def __init__(self, img):

        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.speedx = 0
        self.speedy = 8

    def update(self):

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.y > HEIGHT:
            self.rect.y = -39

class Carro(pygame.sprite.Sprite):
    def __init__(self, img):

        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.speedx = 0
        self.speedy = 4
        self.rect.centerx = WIDTH /2
        self.rect.bottom = HEIGHT - 100

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
    def __init__(self, img):

        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.speedx = 0
        self.speedy = random.randint(1,4)
        self.rect.centerx = posicoesx_iniciais[random.randint(0,3)]
        self.rect.bottom = posicoesy_iniciais[random.randint(0,9)]

    def update(self):

        self.rect.x += self.speedx
        self.rect.y += self.speedy 


        if self.rect.y > HEIGHT:
            self.rect.centerx = posicoesx_iniciais[random.randint(0,3)]
            self.rect.bottom = posicoesy_iniciais[random.randint(0,9)]

class Fundo(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.speedx = 0
        self.speedy = 14

    def update(self):

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.y > (2*HEIGHT):
            self.rect.y = -HEIGHT

class Explosion(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, center, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Armazena a animação de explosão
        self.explosion_anim = assets['explosion_anim']

        # Inicia o processo de animação colocando a primeira imagem na tela.
        self.frame = 0  # Armazena o índice atual na animação
        self.image = self.explosion_anim[self.frame]  # Pega a primeira imagem
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


all_sprites = pygame.sprite.Group()
all_pistas = pygame.sprite.Group()
all_npcs = pygame.sprite.Group()

fundo_1 = Fundo(paisagem_img)
fundo_1.rect.y = -HEIGHT
all_sprites.add(fundo_1)
fundo_2 = Fundo(paisagem_img)
fundo_2.rect.y = 0
all_sprites.add(fundo_2)
fundo_3 = Fundo(paisagem_img)
fundo_3.rect.y = HEIGHT
all_sprites.add(fundo_3)

for i in range(16):
    pista = Pista(pista_img)
    pista.rect.y = 40 * i 
    all_pistas.add(pista)
    all_sprites.add(pista)

for l in range(8):
    npc = NPC(lista_img_npcs[random.randint(0,3)])
    all_npcs.add(npc)
    all_sprites.add(npc)

carro = Carro(carro_img)
all_sprites.add(carro)

Pontuacao = 0

# ===== Loop principal =====
pygame.mixer.music.play(loops=-1)
while game:
    clock.tick(FPS)


    # ----- SOM
    carro_correndo.play()

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
        explosao = Explosion(carro.rect.center, assets)
        all_sprites.add(explosao)
        carro_correndo.stop()
        carro_batida.play()
        time.sleep(1.5)
        game = False 
    
    if len(hits) > 0:
        explosao = Explosion(carro.rect.center, assets)
        all_sprites.add(explosao)
        carro_correndo.stop()
        carro_batida.play()
        time.sleep(1.5)
        game = False 

    all_pistas.update()
    all_npcs.update()
    all_sprites.update()
    Pontuacao += 1

    # ----- Gera saídas

    window.fill((150, 0, 0))  # Preenche com a cor branca
    all_sprites.draw(window)
    
    text_surface = Fonte.render("{:08}".format(Pontuacao), True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (((WIDTH / 2)+2),  10)
    window.blit(text_surface, text_rect)
    
    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados