import pygame
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coletar Itens - Multiplayer")

# Cores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Variáveis dos jogadores
player1_pos = [WIDTH // 4, HEIGHT // 2]
player2_pos = [WIDTH * 3 // 4, HEIGHT // 2]
player_size = 50
score1 = 0
score2 = 0

# Lista para armazenar itens
items = []

# Função para gerar itens
def create_item():
    x = random.randint(0, WIDTH - 30)
    y = random.randint(0, HEIGHT - 30)
    items.append([x, y])

# Loop principal
running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Movimento do jogador 1 (WASD)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player1_pos[0] > 0:
        player1_pos[0] -= 5
    if keys[pygame.K_d] and player1_pos[0] < WIDTH - player_size:
        player1_pos[0] += 5
    if keys[pygame.K_w] and player1_pos[1] > 0:
        player1_pos[1] -= 5
    if keys[pygame.K_s] and player1_pos[1] < HEIGHT - player_size:
        player1_pos[1] += 5
    
    # Movimento do jogador 2 (setas)
    if keys[pygame.K_LEFT] and player2_pos[0] > 0:
        player2_pos[0] -= 5
    if keys[pygame.K_RIGHT] and player2_pos[0] < WIDTH - player_size:
        player2_pos[0] += 5
    if keys[pygame.K_UP] and player2_pos[1] > 0:
        player2_pos[1] -= 5
    if keys[pygame.K_DOWN] and player2_pos[1] < HEIGHT - player_size:
        player2_pos[1] += 5
    
    # Desenha os jogadores
    pygame.draw.rect(screen, GREEN, (player1_pos[0], player1_pos[1], player_size, player_size))
    pygame.draw.rect(screen, RED, (player2_pos[0], player2_pos[1], player_size, player_size))
    
    # Criação de itens
    if random.randint(1, 100) < 5:  # Chance de criar um item
        create_item()
    
    # Desenha itens e verifica colisões
    for item in items[:]:
        pygame.draw.circle(screen, RED, item, 15)
        if (player1_pos[0] < item[0] < player1_pos[0] + player_size and
            player1_pos[1] < item[1] < player1_pos[1] + player_size):
            items.remove(item)
            score1 += 1
        elif (player2_pos[0] < item[0] < player2_pos[0] + player_size and
              player2_pos[1] < item[1] < player2_pos[1] + player_size):
            items.remove(item)
            score2 += 1

    # Exibe a pontuação
    font = pygame.font.Font(None, 36)
    text1 = font.render(f'Score Player 1: {score1}', True, (255, 255, 255))
    text2 = font.render(f'Score Player 2: {score2}', True, (255, 255, 255))
    screen.blit(text1, (10, 10))
    screen.blit(text2, (WIDTH - 200, 10))

    # Atualiza a tela
    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
