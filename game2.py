import pygame
import math

# Inicializa o pygame
pygame.init()

# Informações da tela para resolução total
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("RPG")

# Cores
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Configurações do personagem
player_size = 40
player_center = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5
attack_duration = 1000  # 1 segundo

# Configurações do mapa
MAP_WIDTH, MAP_HEIGHT = 2000, 2000  # Tamanho do mapa maior que a tela
camera_offset = [0, 0]  # Para controlar o deslocamento da câmera

# Obstáculos (árvores) como barreiras
trees = [(300, 400), (600, 200), (800, 1000), (1200, 500)]

# Variáveis de controle do ataque
attacking = False
attack_start_time = 0
attack_line = None

# Função para desenhar o jogador com pernas simples
def draw_player(position, moving):
    body_rect = pygame.Rect(position[0] - player_size // 2, position[1] - player_size // 2, player_size, player_size)
    pygame.draw.rect(screen, WHITE, body_rect)

    # Simples animação de pernas
    if moving:
        pygame.draw.line(screen, RED, (position[0] - 10, position[1] + 20), (position[0] - 20, position[1] + 30), 5)
        pygame.draw.line(screen, RED, (position[0] + 10, position[1] + 20), (position[0] + 20, position[1] + 30), 5)
    else:
        pygame.draw.line(screen, RED, (position[0] - 10, position[1] + 20), (position[0] - 10, position[1] + 30), 5)
        pygame.draw.line(screen, RED, (position[0] + 10, position[1] + 20), (position[0] + 10, position[1] + 30), 5)

# Função para disparar o ataque
def fire_attack(player_pos, target_pos):
    global attack_line, attacking, attack_start_time
    attacking = True
    attack_start_time = pygame.time.get_ticks()

    dx = target_pos[0] - player_center[0]
    dy = target_pos[1] - player_center[1]
    angle = math.atan2(dy, dx)
    end_pos = (player_center[0] + math.cos(angle) * 500, player_center[1] + math.sin(angle) * 500)
    attack_line = (player_center[0], player_center[1], *end_pos)

# Função para desenhar árvores
def draw_trees():
    for tree in trees:
        tree_x, tree_y = tree[0] - camera_offset[0], tree[1] - camera_offset[1]
        pygame.draw.circle(screen, (0, 100, 0), (tree_x, tree_y), 30)

# Função de colisão simples (com árvores e limites)
def is_colliding_with_trees(player_pos):
    player_rect = pygame.Rect(player_pos[0] - player_size // 2, player_pos[1] - player_size // 2, player_size, player_size)
    for tree in trees:
        tree_rect = pygame.Rect(tree[0] - 30, tree[1] - 30, 60, 60)  # Considera o raio das árvores
        if player_rect.colliderect(tree_rect):
            return True
    return False

def check_bounds(new_camera_offset):
    # Mantém a câmera dentro dos limites do mapa
    if new_camera_offset[0] < 0:
        new_camera_offset[0] = 0
    if new_camera_offset[1] < 0:
        new_camera_offset[1] = 0
    if new_camera_offset[0] > MAP_WIDTH - SCREEN_WIDTH:
        new_camera_offset[0] = MAP_WIDTH - SCREEN_WIDTH
    if new_camera_offset[1] > MAP_HEIGHT - SCREEN_HEIGHT:
        new_camera_offset[1] = MAP_HEIGHT - SCREEN_HEIGHT
    return new_camera_offset

# Loop principal
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(GREEN)  # Preenche o fundo com verde (grama)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            fire_attack(player_center, pygame.mouse.get_pos())

    # Movimentação do jogador
    keys = pygame.key.get_pressed()
    moving = False
    new_camera_offset = camera_offset[:]

    if keys[pygame.K_w]:
        new_camera_offset[1] -= player_speed
        moving = True
    if keys[pygame.K_s]:
        new_camera_offset[1] += player_speed
        moving = True
    if keys[pygame.K_a]:
        new_camera_offset[0] -= player_speed
        moving = True
    if keys[pygame.K_d]:
        new_camera_offset[0] += player_speed
        moving = True

    # Verifica colisão com árvores e limites do mapa
    if not is_colliding_with_trees([player_center[0] + new_camera_offset[0], player_center[1] + new_camera_offset[1]]):
        camera_offset = check_bounds(new_camera_offset)

    # Desenha o cenário
    draw_trees()  # Desenha árvores no cenário

    # Desenha o personagem
    draw_player(player_center, moving)

    # Verifica e desenha o ataque
    if attacking:
        pygame.draw.line(screen, WHITE, (attack_line[0], attack_line[1]), (attack_line[2], attack_line[3]), 5)
        if pygame.time.get_ticks() - attack_start_time > attack_duration:
            attacking = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
