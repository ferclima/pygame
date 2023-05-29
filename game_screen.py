import pygame
from config import FPS, WIDTH, HEIGHT, ENDI
from assets import load_assets, BOOM_SOUND, PAISAGEM, SCORE_FONT
from sprites import Pista, Carro, Fundo, NPC, Explosion


def game_screen(window):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    Pontuacao = 0

    assets = load_assets()

    # Criando um grupo de meteoros
    all_sprites = pygame.sprite.Group()
    all_pistas = pygame.sprite.Group()
    all_npcs = pygame.sprite.Group()
    all_backgrounds = pygame.sprite.Group()

    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_pistas'] = all_pistas
    groups['all_NPCs'] = all_npcs
    groups['all_backgrounds'] = all_backgrounds

    # Criando fundos
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

    # Criando pistas
    for i in range(16):
        pista = Pista(groups, assets)
        pista.rect.y = 40 * i 
        all_pistas.add(pista)
        all_sprites.add(pista)

    # Criando NPCs
    for l in range(8):
        npc = NPC(groups, assets)
        all_npcs.add(npc)
        all_sprites.add(npc)

    # Criando Jogador
    carro = Carro(groups, assets)
    all_sprites.add(carro)


    PLAYING = 1
    EXPLODING = 2
    state = PLAYING
    game = True

    # ===== Loop principal =====
    pygame.mixer.music.play(loops=-1)
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
        fundo_1.pontuacao = Pontuacao
        fundo_2.pontuacao = Pontuacao
        fundo_3.pontuacao = Pontuacao

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
                state = ENDI   
                with open ('PONTUACAO.txt', 'a') as Arquivo:
                    Arquivo.write("{0}, ".format(Pontuacao))
                return state

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
    #pygame.quit()  # Função do PyGame que finaliza os recursos utilizados