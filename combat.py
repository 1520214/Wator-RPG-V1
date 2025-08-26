import pygame
import math

class CombatSystem:
    def __init__(self):
        self.projectiles = []
        
    def player_attack(self, player, enemies):
        if not player.player_class:
            return
            
        # Ataque básico baseado na classe
        if player.player_class.value == "warrior":
            self._warrior_attack(player, enemies)
        elif player.player_class.value == "mage":
            self._mage_attack(player, enemies)
        elif player.player_class.value == "thief":
            self._thief_attack(player, enemies)
            
    def _warrior_attack(self, player, enemies):
        # Ataque corpo a corpo em área
        attack_range = 60
        damage = 30
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - player.x)**2 + (enemy.y - player.y)**2)
            if distance <= attack_range:
                enemy.take_damage(damage)
                
    def _mage_attack(self, player, enemies):
        # Cria projétil mágico
        if player.current_mana >= 10:
            player.current_mana -= 10
            
            # Encontra o inimigo mais próximo
            closest_enemy = None
            min_distance = float('inf')
            
            for enemy in enemies:
                distance = math.sqrt((enemy.x - player.x)**2 + (enemy.y - player.y)**2)
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
                    
            if closest_enemy:
                projectile = MagicProjectile(player.x, player.y, closest_enemy.x, closest_enemy.y)
                self.projectiles.append(projectile)
                
    def _thief_attack(self, player, enemies):
        # Ataque rápido com chance de crítico
        attack_range = 40
        base_damage = 25
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - player.x)**2 + (enemy.y - player.y)**2)
            if distance <= attack_range:
                # 30% de chance de crítico
                import random
                damage = base_damage * 2 if random.random() < 0.3 else base_damage
                enemy.take_damage(damage)
                
    def update(self, enemies):
        # Atualiza projéteis
        for projectile in self.projectiles[:]:
            projectile.update()
            
            # Verifica colisão com inimigos
            for enemy in enemies:
                if projectile.check_collision(enemy):
                    enemy.take_damage(projectile.damage)
                    self.projectiles.remove(projectile)
                    break
                    
            # Remove projéteis que saíram da tela
            if projectile.is_off_screen():
                self.projectiles.remove(projectile)
                
    def draw(self, screen):
        for projectile in self.projectiles:
            projectile.draw(screen)

class MagicProjectile:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.x = start_x
        self.y = start_y
        self.speed = 8
        self.damage = 40
        self.radius = 6
        
        # Calcula direção
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.dx = (dx / distance) * self.speed
            self.dy = (dy / distance) * self.speed
        else:
            self.dx = 0
            self.dy = 0
            
    def update(self):
        self.x += self.dx
        self.y += self.dy
        
    def check_collision(self, enemy):
        distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
        return distance <= self.radius + 12  # 12 é metade do tamanho do inimigo
        
    def is_off_screen(self):
        return self.x < -50 or self.x > 850 or self.y < -50 or self.y > 650
        
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 100, 255), (int(self.x), int(self.y)), self.radius)

