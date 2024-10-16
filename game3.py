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
BLACK = (0, 0, 0)

# Configurações do personagem
player_size = 40
player_center = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5
attack_duration = 1000  # 1 segundo

# Configurações do mapa
MAP_WIDTH, MAP_HEIGHT = 6000, 6000  # Diminui o tamanho do mapa para mais movimento
camera_offset = [0, 0]  # Para controlar o deslocamento da câmera

# Obstáculos (árvores) como barreiras
trees = [(300, 400), (600, 200), (800, 600), (1200, 500), (900, 700), (700, 800), (1100, 300)]

# Inventário e coleta de madeira
inventory = {"wood": 0}
tree_hits = {tree: 0 for tree in trees}  # Contador de batidas por árvore

# Função para desenhar o jogador com braços, pernas e olhos
def draw_player(position, moving, breaking):
    body_rect = pygame.Rect(position[0] - player_size // 2, position[1] - player_size // 2, player_size, player_size)
    pygame.draw.rect(screen, WHITE, body_rect)

    # Olhos
    pygame.draw.circle(screen, BLACK, (position[0] - 10, position[1] - 10), 5)
    pygame.draw.circle(screen, BLACK, (position[0] + 10, position[1] - 10), 5)

    # Braços (simula movimento de bater ao quebrar árvore)
    if breaking:
        pygame.draw.line(screen, RED, (position[0] + 20, position[1] - 10), (position[0] + 40, position[1]), 5)
    else:
        pygame.draw.line(screen, RED, (position[0] + 20, position[1] - 10), (position[0] + 30, position[1]), 5)

    # Simples animação de pernas
    if moving:
        pygame.draw.line(screen, RED, (position[0] - 10, position[1] + 20), (position[0] - 20, position[1] + 30), 5)
        pygame.draw.line(screen, RED, (position[0] + 10, position[1] + 20), (position[0] + 20, position[1] + 30), 5)
    else:
        pygame.draw.line(screen, RED, (position[0] - 10, position[1] + 20), (position[0] - 10, position[1] + 30), 5)
        pygame.draw.line(screen, RED, (position[0] + 10, position[1] + 20), (position[0] + 10, position[1] + 30), 5)

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

# Função para simular o corte da árvore e coleta de madeira
def chop_tree(player_pos, mouse_pos):
    for tree in trees:
        tree_x, tree_y = tree[0] - camera_offset[0], tree[1] - camera_offset[1]
        distance = math.sqrt((tree_x - player_pos[0]) ** 2 + (tree_y - player_pos[1]) ** 2)
        if distance < 50:  # Se estiver perto o suficiente da árvore
            tree_hits[tree] += 1
            if tree_hits[tree] == 3:  # A cada 3 batidas, coleta 1 madeira
                inventory["wood"] += 1
                tree_hits[tree] = 0  # Reseta o contador de batidas
            return True
    return False

# Loop principal
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(GREEN)  # Preenche o fundo com verde (grama)

    breaking = False  # Se está quebrando uma árvore ou não
    moving = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botão esquerdo do mouse
                breaking = chop_tree(player_center, pygame.mouse.get_pos())

    # Movimentação do jogador
    keys = pygame.key.get_pressed()
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
    draw_player(player_center, moving, breaking)

    # Mostra o inventário na tela
    font = pygame.font.SysFont(None, 36)
    wood_text = font.render(f"Wood: {inventory['wood']}", True, BLACK)
    screen.blit(wood_text, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
