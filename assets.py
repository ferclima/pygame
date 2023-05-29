import pygame
import os
from config import WIDTH, HEIGHT, WIDTH_CARRO, HEIGHT_CARRO, WIDTH_NPC, HEIGHT_NPC, IMG_DIR, SND_DIR, FNT_DIR


PAISAGEM = 'paisagem'
PISTA_IMG = 'pista'
CARRO_IMG = 'carro'
NPC_IMG = 'NPCs'
EXPLOSION_ANIM = 'explosion_anim'
SCORE_FONT = 'fonte'
BOOM_SOUND = 'boom_sound'


def load_assets():
    assets = {}
    paisagem_1 = pygame.image.load('Imagens\Floresta2..png').convert_alpha()
    paisagem_1 = pygame.transform.scale(paisagem_1, (WIDTH, HEIGHT))
    paisagem_2 = pygame.image.load('Imagens\deserto2.png').convert_alpha()
    paisagem_2 = pygame.transform.scale(paisagem_2, (WIDTH, HEIGHT))
    paisagem_3 = pygame.image.load('Imagens\Gelo2.png').convert_alpha()
    paisagem_3 = pygame.transform.scale(paisagem_3, (WIDTH, HEIGHT))
    paisagem_4 = pygame.image.load('Imagens\Inether2.png').convert_alpha()
    paisagem_4 = pygame.transform.scale(paisagem_4, (WIDTH, HEIGHT))
    assets['paisagem'] = [paisagem_1, paisagem_2, paisagem_3, paisagem_4]
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
    pygame.mixer.music.load('Sons\Life is a Highway.mp3')
    pygame.mixer.music.set_volume(0.4)
    #pygame.mixer.music.load('Sons\carro-explosao2.mp3')
    assets['aceleração'] = pygame.mixer.Sound('Sons\carro-correndo-loop.mp3')
    assets['batida'] = pygame.mixer.Sound('Sons\carro-explosao2.mp3')
    return assets