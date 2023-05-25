import pygame
import random
from os import path

from config import IMG_DIR, FPS, GAME, QUIT, WIDTH


def quit_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    #background = pygame.image.load(path.join(IMG_DIR, 'Tela inicial.png')).convert()
    #background_rect = background.get_rect()

    fonte = pygame.font.Font('fonte\PressStart2P.ttf', 25)
    fonte_2 = pygame.font.Font('fonte\PressStart2P.ttf', 20)
    fonte_3 = pygame.font.Font('fonte\PressStart2P.ttf', 15)

    with open('PONTUACAO.txt', 'r') as Arquivo:
        conteudo = Arquivo.read()

    lista_pontuacoes = conteudo.split(', ')
    del lista_pontuacoes[-1]
    lista_pontuacoes = list(map(int, lista_pontuacoes))
    pontuacao_jogador = lista_pontuacoes[-1]
    lista_pontuacoes.sort(reverse=True)
    posicao_rank = lista_pontuacoes.index(pontuacao_jogador)


    running = True
    while running:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = QUIT
                running = False

        # A cada loop, redesenha o fundo e os sprites
        screen.fill((0,0,0))
        texto_1 = fonte.render('RANKING', True, (255, 255, 255))
        rect_texto_1 = texto_1.get_rect()
        rect_texto_1.midtop = ((WIDTH / 2),  10)
        screen.blit(texto_1, rect_texto_1)

        texto_2 = fonte_2.render(('Sua pontuação foi: {0}'.format(pontuacao_jogador)), True, (255, 255, 255))
        rect_texto_2 = texto_2.get_rect()
        rect_texto_2.midtop = ((WIDTH / 2),  (rect_texto_1.bottom + 10))
        screen.blit(texto_2, rect_texto_2)

        texto_3 = fonte_3.render(('Você é o {0}º colocado no ranking'.format(posicao_rank+1)), True, (255, 255, 255))
        rect_texto_3 = texto_3.get_rect()
        rect_texto_3.midtop = ((WIDTH / 2),  (rect_texto_2.bottom + 10))
        screen.blit(texto_3, rect_texto_3)

        esp = 110
        for h in range(1,11):
            texto = fonte_2.render(('{0}º- {1}'.format(h, lista_pontuacoes[h-1])), True, (255, 255, 255))
            rect_texto = texto.get_rect()
            rect_texto.midtop = ((WIDTH / 2),  esp)
            screen.blit(texto, rect_texto)
            esp += 50 

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state