# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame

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
pista_img = pygame.image.load('Mini pista.png').convert_alpha()
carro_img = pygame.image.load('Carrinho v1.png').convert_alpha()
carro_img = pygame.transform.scale(carro_img, (50, 38))

class Pista(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = 0
        self.speedx = 0
        self.speedy = 5

    def update(self):
        # Atualizando a posição do meteoro
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Se o meteoro passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.y > HEIGHT:
            self.kill()
class Carro(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH /2
        self.rect.bottom = HEIGHT - 10

all_sprites = pygame.sprite.Group()
all_pistas = pygame.sprite.Group()
pista = Pista(pista_img)
carro = Carro(carro_img)
all_pistas.add(pista)
all_sprites.add(pista)
all_sprites.add(carro)

# ===== Loop principal =====
while game:
    clock.tick(FPS)

    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            game = False

    if pista.rect.y == 40:
        pista = Pista(pista_img)
        all_pistas.add(pista)
        all_sprites.add(pista)

    all_pistas.update()
    all_sprites.update()

    # ----- Gera saídas

    window.fill((150, 0, 0))  # Preenche com a cor branca
    
    all_sprites.draw(window)

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados