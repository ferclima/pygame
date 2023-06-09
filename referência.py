# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
from config import WIDTH, HEIGHT, INIC, GAME, QUIT, ENDI
from init_screen import init_screen
from game_screen import game_screen
from quit_screen import quit_screen


pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Race Mania')

state = INIC
while state != QUIT:
    if state == INIC:
        state = init_screen(window)
    elif state == GAME:
        state = game_screen(window)
    elif state == ENDI:
        state = quit_screen(window)

# ===== Finalização =====
pygame.quit() 