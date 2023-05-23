# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
import time

pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
WIDTH = 500
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Race Mania')

# ----- Inicia estruturas de dados
clock = pygame.time.Clock()
FPS = 40
game = True
WIDTH_CARRO = 27
HEIGHT_CARRO = 50
WIDTH_NPC = 27
HEIGHT_NPC = 50
WIDTH_PISTA = 208
HEIGHT_PISTA = 40

assets = {}
paisagem_1 = pygame.image.load('Imagens\Paisagem2..png').convert_alpha()
paisagem_1 = pygame.transform.scale(paisagem_1, (WIDTH, HEIGHT))
paisagem_2 = pygame.image.load('Imagens\paisagem-deserto.png').convert_alpha()
paisagem_2 = pygame.transform.scale(paisagem_2, (WIDTH, HEIGHT))
assets['paisagem'] = [paisagem_1, paisagem_2]
assets['pista'] = pygame.image.load('Imagens\Mini pista.png').convert_alpha()
assets['carro'] = pygame.image.load('Imagens\carrinho2-removebg-preview.png').convert_alpha()
assets['carro'] = pygame.transform.scale(assets['carro'], (WIDTH_CARRO, HEIGHT_CARRO))
assets['fonte'] = pygame.font.Font('fonte\PressStart2P.ttf', 25)
npc_img1 = pygame.image.load('Imagens\obstaculo 1.png').convert_alpha()
npc_img1 = pygame.transform.scale(npc_img1, (WIDTH_NPC, HEIGHT_CARRO))
npc_img2 = pygame.image.load('Imagens\obstaculo 2.png').convert_alpha()
npc_img2 = pygame.transform.scale(npc_img2, (WIDTH_NPC, HEIGHT_NPC))
npc_img3 = pygame.image.load('Imagens\obstaculo 3.png').convert_alpha()
npc_img3 = pygame.transform.scale(npc_img3, (WIDTH_NPC, HEIGHT_NPC))
npc_img4 = pygame.image.load('Imagens\obstaculo 4.png').convert_alpha()
npc_img4 = pygame.transform.scale(npc_img4, (WIDTH_NPC, HEIGHT_NPC))
assets['NPCs'] = [npc_img1, npc_img2, npc_img3, npc_img4]
explosion_anim = []
for i in range(9):
    # Os arquivos de animação são numerados de 00 a 08
    filename = "Explosão\Explosion0{}.png".format(i)
    img = pygame.image.load(filename).convert_alpha()
    img = pygame.transform.scale(img, (32, 32))
    explosion_anim.append(img)
assets["explosion_anim"] = explosion_anim
# ===== Loading dos sons do carro
pygame.mixer.music.load('Sons\carro-correndo-loop.mp3')
pygame.mixer.music.set_volume(0.4)
#pygame.mixer.music.load('Sons\carro-explosao2.mp3')
assets['aceleração'] = pygame.mixer.Sound('Sons\carro-correndo-loop.mp3')
assets['batida'] = pygame.mixer.Sound('Sons\carro-explosao2.mp3')

posicoesx_iniciais = [175, 225, 275, 325]
posicoesy_iniciais = [0, -100, -200, -300, -400, -500, -600, -700, -800, -900]

Pontuacao = 0


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
    def __init__(self, groups, assets):

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

    def update(self):

        self.rect.x += self.speedx
        self.rect.y += self.speedy 


        if self.rect.y > HEIGHT:
            self.rect.centerx = posicoesx_iniciais[random.randint(0,3)]
            self.rect.bottom = posicoesy_iniciais[random.randint(0,9)]

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

    def update(self):

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.y > (2*HEIGHT):
            self.rect.y = -HEIGHT

        if Pontuacao > 2000:
            self.image = assets['paisagem'][1]


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


all_sprites = pygame.sprite.Group()
all_pistas = pygame.sprite.Group()
all_npcs = pygame.sprite.Group()
all_backgrounds = pygame.sprite.Group()

groups = {}
groups['all_sprites'] = all_sprites
groups['all_pistas'] = all_pistas
groups['all_NPCs'] = all_npcs
groups['all_backgrounds'] = all_backgrounds

fundo_1 = Fundo(groups, assets)
fundo_1.rect.y = -HEIGHT
all_backgrounds.add(fundo_1)
all_sprites.add(fundo_1)

fundo_2 = Fundo(groups, assets)
fundo_2.rect.y = 0
all_backgrounds.add(fundo_2)
all_sprites.add(fundo_2)

fundo_3 = Fundo(groups, assets)
fundo_3.rect.y = HEIGHT
all_backgrounds.add(fundo_3)
all_sprites.add(fundo_3)

for i in range(16):
    pista = Pista(groups, assets)
    pista.rect.y = 40 * i 
    all_pistas.add(pista)
    all_sprites.add(pista)

for l in range(8):
    npc = NPC(groups, assets)
    all_npcs.add(npc)
    all_sprites.add(npc)

carro = Carro(groups, assets)
all_sprites.add(carro)


PLAYING = 1
EXPLODING = 2
state = PLAYING

# ===== Loop principal =====
#pygame.mixer.music.play(loops=-1)
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
                assets['aceleração'].play()
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
                assets['aceleração'].stop()
            if event.key == pygame.K_DOWN:
                carro.speedy -= 4
        
    all_pistas.update()
    all_npcs.update()
    all_backgrounds.update()
    all_sprites.update()
    Pontuacao += 1

    if state == PLAYING:

        hits = pygame.sprite.spritecollide(carro, all_npcs, True, pygame.sprite.collide_mask)
    
        if len(hits) > 0 or carro.rect.centerx > 354 or carro.rect.centerx < 146:
            assets['aceleração'].stop()
            assets['batida'].play()
            carro.kill()
            explosao = Explosion(carro.rect.center, assets)
            all_sprites.add(explosao)
            state = EXPLODING
            keys_down = {}
            explosion_tick = pygame.time.get_ticks()
            explosion_duration = explosao.frame_ticks * len(explosao.explosion_anim) + 400

    elif state == EXPLODING:
        now = pygame.time.get_ticks()
        if now - explosion_tick > explosion_duration:
            assets['batida'].play()
            game = False        

    # ----- Gera saídas

    window.fill((0, 150, 0))  # Preenche com a cor verde
    all_sprites.draw(window)
    
    text_surface = assets['fonte'].render("{:08}".format(Pontuacao), True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (((WIDTH / 2)+2),  10)
    window.blit(text_surface, text_rect)
    
    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados