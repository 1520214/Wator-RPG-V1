import pygame
import sys
from game_state import GameState, GameStateManager
from player import Player, PlayerClass
from ui import UI
from enemy import EnemySpawner
from combat import CombatSystem

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Renascimento do Zero")
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 100, 0)

# Inicializa sistemas do jogo
game_state_manager = GameStateManager()
ui = UI(SCREEN_WIDTH, SCREEN_HEIGHT)
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
enemy_spawner = EnemySpawner(SCREEN_WIDTH, SCREEN_HEIGHT)
combat_system = CombatSystem()

# Variáveis de controle
keys_pressed = set()
attack_cooldown = 0

def handle_menu_input(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            game_state_manager.change_state(GameState.CLASS_SELECTION)
        elif event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

def handle_class_selection_input(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
            player.set_class(PlayerClass.WARRIOR)
            game_state_manager.change_state(GameState.PLAYING)
        elif event.key == pygame.K_2:
            player.set_class(PlayerClass.MAGE)
            game_state_manager.change_state(GameState.PLAYING)
        elif event.key == pygame.K_3:
            player.set_class(PlayerClass.THIEF)
            game_state_manager.change_state(GameState.PLAYING)

def handle_playing_input(event):
    global attack_cooldown
    
    if event.type == pygame.KEYDOWN:
        keys_pressed.add(event.key)
        
        # Ataque
        if event.key == pygame.K_SPACE and attack_cooldown == 0:
            combat_system.player_attack(player, enemy_spawner.get_enemies())
            attack_cooldown = 30  # 0.5 segundos a 60 FPS
            
    elif event.type == pygame.KEYUP:
        keys_pressed.discard(event.key)

def handle_game_over_input(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            # Renascimento
            player.rebirth()
            enemy_spawner.enemies.clear()
            combat_system.projectiles.clear()
            game_state_manager.change_state(GameState.CLASS_SELECTION)
        elif event.key == pygame.K_m:
            # Volta ao menu
            player.__init__(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            enemy_spawner.enemies.clear()
            combat_system.projectiles.clear()
            game_state_manager.change_state(GameState.MENU)

def update_playing():
    global attack_cooldown
    
    # Reduz cooldown de ataque
    if attack_cooldown > 0:
        attack_cooldown -= 1
    
    # Movimento do jogador
    dx, dy = 0, 0
    if pygame.K_LEFT in keys_pressed or pygame.K_a in keys_pressed:
        dx = -1
    if pygame.K_RIGHT in keys_pressed or pygame.K_d in keys_pressed:
        dx = 1
    if pygame.K_UP in keys_pressed or pygame.K_w in keys_pressed:
        dy = -1
    if pygame.K_DOWN in keys_pressed or pygame.K_s in keys_pressed:
        dy = 1
        
    # Normaliza movimento diagonal
    if dx != 0 and dy != 0:
        dx *= 0.707
        dy *= 0.707
        
    player.move(dx, dy)
    
    # Mantém o jogador na tela
    player.x = max(16, min(SCREEN_WIDTH - 16, player.x))
    player.y = max(16, min(SCREEN_HEIGHT - 16, player.y))
    player.rect.x = player.x
    player.rect.y = player.y
    
    # Atualiza sistemas
    enemy_spawner.update(player)
    combat_system.update(enemy_spawner.get_enemies())
    
    # Verifica se o jogador morreu
    if player.current_health <= 0:
        game_state_manager.change_state(GameState.GAME_OVER)

def draw_playing():
    screen.fill(DARK_GREEN)
    
    # Desenha elementos do jogo
    player.draw(screen)
    enemy_spawner.draw(screen)
    combat_system.draw(screen)
    
    # Desenha UI
    ui.draw_health_bar(screen, player)
    ui.draw_mana_bar(screen, player)
    ui.draw_player_info(screen, player)
    
    # Instruções
    font = pygame.font.Font(None, 24)
    instructions = [
        "WASD/Setas: Mover",
        "ESPAÇO: Atacar"
    ]
    
    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, WHITE)
        screen.blit(text, (20, SCREEN_HEIGHT - 60 + i * 25))

# Game loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Gerencia input baseado no estado atual
        current_state = game_state_manager.get_current_state()
        
        if current_state == GameState.MENU:
            handle_menu_input(event)
        elif current_state == GameState.CLASS_SELECTION:
            handle_class_selection_input(event)
        elif current_state == GameState.PLAYING:
            handle_playing_input(event)
        elif current_state == GameState.GAME_OVER:
            handle_game_over_input(event)
    
    # Atualiza lógica do jogo
    current_state = game_state_manager.get_current_state()
    
    if current_state == GameState.PLAYING:
        update_playing()
    
    # Renderiza baseado no estado atual
    if current_state == GameState.MENU:
        ui.draw_menu(screen)
    elif current_state == GameState.CLASS_SELECTION:
        ui.draw_class_selection(screen)
    elif current_state == GameState.PLAYING:
        draw_playing()
    elif current_state == GameState.GAME_OVER:
        draw_playing()  # Desenha o jogo no fundo
        ui.draw_game_over(screen)
    
    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

# Encerra o Pygame
pygame.quit()
sys.exit()


