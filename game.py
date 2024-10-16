import pygame
import math
import keyboard

# Inicializa o pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("RPG")

# Cores
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)

# Configurações do personagem
player_size = 40
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5
attack_duration = 1000  # 1 segundo

# Variáveis de controle do ataque
attacking = False
attack_start_time = 0
attack_line = None

# Função para desenhar o jogador
def draw_player(position):
    pygame.draw.rect(screen, WHITE, (*position, player_size, player_size))

# Função para disparar o ataque
def fire_attack(player_pos, target_pos):
    global attack_line, attacking, attack_start_time
    attacking = True
    attack_start_time = pygame.time.get_ticks()
    
    dx = target_pos[0] - player_pos[0]
    dy = target_pos[1] - player_pos[1]
    angle = math.atan2(dy, dx)
    end_pos = (player_pos[0] + math.cos(angle) * 500, player_pos[1] + math.sin(angle) * 500)
    attack_line = (player_pos[0] + player_size // 2, player_pos[1] + player_size // 2, *end_pos)

# Função para desenhar árvores (apenas exemplo)
def draw_trees():
    for i in range(50):
        tree_x = i * 60 % SCREEN_WIDTH
        tree_y = (i // 13) * 80
        pygame.draw.circle(screen, (0, 100, 0), (tree_x, tree_y), 30)

# Loop principal
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(GREEN)  # Preenche o fundo com verde (grama)
    draw_trees()  # Desenha árvores no cenário

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            fire_attack(player_pos, pygame.mouse.get_pos())

    # Movimentação do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos[1] -= player_speed
    if keys[pygame.K_s]:
        player_pos[1] += player_speed
    if keys[pygame.K_a]:
        player_pos[0] -= player_speed
    if keys[pygame.K_d]:
        player_pos[0] += player_speed

    # Desenha o personagem
    draw_player(player_pos)

    # Verifica e desenha o ataque
    if attacking:
        pygame.draw.line(screen, WHITE, (attack_line[0], attack_line[1]), (attack_line[2], attack_line[3]), 5)
        if pygame.time.get_ticks() - attack_start_time > attack_duration:
            attacking = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
