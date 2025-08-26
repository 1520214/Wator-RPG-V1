import pygame
from player import PlayerClass

class UI:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def draw_health_bar(self, screen, player):
        # Barra de vida
        bar_width = 200
        bar_height = 20
        bar_x = 20
        bar_y = 20
        
        # Fundo da barra
        pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        # Barra de vida atual
        health_ratio = player.current_health / player.max_health
        current_width = int(bar_width * health_ratio)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, current_width, bar_height))
        
        # Texto da vida
        health_text = self.small_font.render(f"HP: {player.current_health}/{player.max_health}", True, (255, 255, 255))
        screen.blit(health_text, (bar_x, bar_y + bar_height + 5))
        
    def draw_mana_bar(self, screen, player):
        # Barra de mana
        bar_width = 200
        bar_height = 20
        bar_x = 20
        bar_y = 70
        
        # Fundo da barra
        pygame.draw.rect(screen, (0, 0, 100), (bar_x, bar_y, bar_width, bar_height))
        
        # Barra de mana atual
        mana_ratio = player.current_mana / player.max_mana
        current_width = int(bar_width * mana_ratio)
        pygame.draw.rect(screen, (0, 0, 255), (bar_x, bar_y, current_width, bar_height))
        
        # Texto da mana
        mana_text = self.small_font.render(f"MP: {player.current_mana}/{player.max_mana}", True, (255, 255, 255))
        screen.blit(mana_text, (bar_x, bar_y + bar_height + 5))
        
    def draw_player_info(self, screen, player):
        # Informações do jogador
        info_x = self.screen_width - 200
        info_y = 20
        
        level_text = self.small_font.render(f"Nível: {player.level}", True, (255, 255, 255))
        screen.blit(level_text, (info_x, info_y))
        
        exp_text = self.small_font.render(f"EXP: {player.experience}/{player.experience_to_next_level}", True, (255, 255, 255))
        screen.blit(exp_text, (info_x, info_y + 25))
        
        if player.player_class:
            class_text = self.small_font.render(f"Classe: {player.player_class.value.capitalize()}", True, (255, 255, 255))
            screen.blit(class_text, (info_x, info_y + 50))
            
        rebirth_text = self.small_font.render(f"Renascimentos: {player.rebirth_count}", True, (255, 255, 255))
        screen.blit(rebirth_text, (info_x, info_y + 75))
        
    def draw_class_selection(self, screen):
        # Tela de seleção de classe
        screen.fill((0, 0, 0))
        
        # Título
        title_text = self.font.render("Escolha sua Classe", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(title_text, title_rect)
        
        # Opções de classe
        classes = [
            ("1 - Guerreiro", "Combatente corpo a corpo com alta defesa"),
            ("2 - Mago", "Lançador de feitiços com magia poderosa"),
            ("3 - Ladrão", "Atacante ágil que elimina seus inimigos")
        ]
        
        y_offset = 200
        for i, (class_name, description) in enumerate(classes):
            class_text = self.font.render(class_name, True, (255, 255, 255))
            desc_text = self.small_font.render(description, True, (200, 200, 200))
            
            class_rect = class_text.get_rect(center=(self.screen_width // 2, y_offset + i * 80))
            desc_rect = desc_text.get_rect(center=(self.screen_width // 2, y_offset + i * 80 + 30))
            
            screen.blit(class_text, class_rect)
            screen.blit(desc_text, desc_rect)
            
    def draw_menu(self, screen):
        # Menu principal
        screen.fill((0, 0, 0))
        
        # Título do jogo
        title_text = self.font.render("Renascimento do Zero", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 200))
        screen.blit(title_text, title_rect)
        
        # Instruções
        start_text = self.small_font.render("Pressione ESPAÇO para começar", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(self.screen_width // 2, 300))
        screen.blit(start_text, start_rect)
        
        quit_text = self.small_font.render("Pressione ESC para sair", True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=(self.screen_width // 2, 330))
        screen.blit(quit_text, quit_rect)
        
    def draw_game_over(self, screen):
        # Tela de game over
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Texto de game over
        game_over_text = self.font.render("Você Morreu!", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        screen.blit(game_over_text, game_over_rect)
        
        # Instruções de renascimento
        rebirth_text = self.small_font.render("Pressione R para renascer", True, (255, 255, 255))
        rebirth_rect = rebirth_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(rebirth_text, rebirth_rect)
        
        menu_text = self.small_font.render("Pressione M para voltar ao menu", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 30))
        screen.blit(menu_text, menu_rect)

