from os import path

# Estabelece a pasta que contem as figuras e sons.
IMG_DIR = path.join(path.dirname(__file__), 'Imagens')
SND_DIR = path.join(path.dirname(__file__), 'Sons')
FNT_DIR = path.join(path.dirname(__file__), 'fonte')

FPS = 40
WIDTH = 500
HEIGHT = 600
WIDTH_CARRO = 27
HEIGHT_CARRO = 50
WIDTH_NPC = 27
HEIGHT_NPC = 50
WIDTH_PISTA = 208
HEIGHT_PISTA = 40

INIC = 0
GAME = 1
QUIT = 2
ENDI = 3