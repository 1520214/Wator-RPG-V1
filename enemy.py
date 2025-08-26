import pygame
import random
import math

class Enemy:
    def __init__(self, x, y, enemy_type="basic"):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.rect = pygame.Rect(x, y, 24, 24)
        
        # Atributos baseados no tipo
        if enemy_type == "basic":
            self.max_health = 50
            self.damage = 10
            self.speed = 2
            self.exp_reward = 25
            self.color = (255, 100, 100)  # Vermelho claro
        elif enemy_type == "strong":
            self.max_health = 100
            self.damage = 20
            self.speed = 1
            self.exp_reward = 50
            self.color = (200, 0, 0)  # Vermelho escuro
        elif enemy_type == "fast":
            self.max_health = 30
            self.damage = 15
            self.speed = 4
            self.exp_reward = 35
            self.color = (255, 255, 0)  # Amarelo
            
        self.current_health = self.max_health
        self.is_alive = True
        
        # IA básica
        self.target = None
        self.attack_cooldown = 0
        self.attack_delay = 60  # 1 segundo a 60 FPS
        
    def update(self, player):
        if not self.is_alive:
            return
            
        # Reduz cooldown de ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # Segue o jogador
        self.target = player
        self._move_towards_target()
        
        # Ataca se estiver próximo
        if self._is_near_target() and self.attack_cooldown == 0:
            self._attack_target()
            
    def _move_towards_target(self):
        if not self.target:
            return
            
        # Calcula direção para o alvo
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Normaliza a direção
            dx /= distance
            dy /= distance
            
            # Move em direção ao alvo
            self.x += dx * self.speed
            self.y += dy * self.speed
            self.rect.x = self.x
            self.rect.y = self.y
            
    def _is_near_target(self):
        if not self.target:
            return False
            
        distance = math.sqrt((self.target.x - self.x)**2 + (self.target.y - self.y)**2)
        return distance < 40
        
    def _attack_target(self):
        if not self.target:
            return
            
        # Causa dano ao jogador
        self.target.current_health -= self.damage
        self.attack_cooldown = self.attack_delay
        
        # Verifica se o jogador morreu
        if self.target.current_health <= 0:
            self.target.current_health = 0
            
    def take_damage(self, damage):
        self.current_health -= damage
        if self.current_health <= 0:
            self.current_health = 0
            self.is_alive = False
            
    def draw(self, screen):
        if not self.is_alive:
            return
            
        # Desenha o inimigo
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Desenha barra de vida se não estiver com vida cheia
        if self.current_health < self.max_health:
            bar_width = 30
            bar_height = 4
            bar_x = self.x - 3
            bar_y = self.y - 8
            
            # Fundo da barra
            pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            
            # Barra de vida atual
            health_ratio = self.current_health / self.max_health
            current_width = int(bar_width * health_ratio)
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, current_width, bar_height))

class EnemySpawner:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_delay = 180  # 3 segundos a 60 FPS
        
    def update(self, player):
        # Atualiza timer de spawn
        self.spawn_timer += 1
        
        # Spawna novos inimigos
        if self.spawn_timer >= self.spawn_delay:
            self._spawn_enemy()
            self.spawn_timer = 0
            
        # Atualiza inimigos existentes
        for enemy in self.enemies[:]:
            if enemy.is_alive:
                enemy.update(player)
            else:
                # Remove inimigos mortos e dá experiência
                player.gain_experience(enemy.exp_reward)
                self.enemies.remove(enemy)
                
    def _spawn_enemy(self):
        # Escolhe um tipo de inimigo aleatório
        enemy_types = ["basic", "strong", "fast"]
        enemy_type = random.choice(enemy_types)
        
        # Spawna fora da tela
        side = random.randint(0, 3)
        if side == 0:  # Topo
            x = random.randint(0, self.screen_width)
            y = -30
        elif side == 1:  # Direita
            x = self.screen_width + 30
            y = random.randint(0, self.screen_height)
        elif side == 2:  # Baixo
            x = random.randint(0, self.screen_width)
            y = self.screen_height + 30
        else:  # Esquerda
            x = -30
            y = random.randint(0, self.screen_height)
            
        enemy = Enemy(x, y, enemy_type)
        self.enemies.append(enemy)
        
    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
            
    def get_enemies(self):
        return [enemy for enemy in self.enemies if enemy.is_alive]

