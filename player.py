import pygame
from enum import Enum

class PlayerClass(Enum):
    WARRIOR = "warrior"
    MAGE = "mage"
    THIEF = "thief"

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        
        # Atributos base
        self.max_health = 100
        self.current_health = self.max_health
        self.max_mana = 50
        self.current_mana = self.max_mana
        
        # Classe do jogador
        self.player_class = None
        self.class_skills = []
        
        # Movimento
        self.speed = 5
        self.rect = pygame.Rect(x, y, 32, 32)
        
        # Memórias de vidas passadas
        self.past_life_memories = []
        self.rebirth_count = 0
        
    def set_class(self, player_class):
        self.player_class = player_class
        self._apply_class_bonuses()
        
    def _apply_class_bonuses(self):
        if self.player_class == PlayerClass.WARRIOR:
            self.max_health = 150
            self.current_health = self.max_health
            self.max_mana = 30
            self.current_mana = self.max_mana
            self.class_skills = ["Ataque Básico", "Escudo Defensivo"]
            
        elif self.player_class == PlayerClass.MAGE:
            self.max_health = 80
            self.current_health = self.max_health
            self.max_mana = 100
            self.current_mana = self.max_mana
            self.class_skills = ["Bola de Fogo", "Escudo Arcano"]
            
        elif self.player_class == PlayerClass.THIEF:
            self.max_health = 100
            self.current_health = self.max_health
            self.max_mana = 60
            self.current_mana = self.max_mana
            self.speed = 7
            self.class_skills = ["Ataque Furtivo", "Esquiva Rápida"]
    
    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.x = self.x
        self.rect.y = self.y
        
    def gain_experience(self, exp):
        self.experience += exp
        if self.experience >= self.experience_to_next_level:
            self.level_up()
            
    def level_up(self):
        self.level += 1
        self.experience -= self.experience_to_next_level
        self.experience_to_next_level = int(self.experience_to_next_level * 1.5)
        
        # Aumenta atributos
        self.max_health += 20
        self.current_health = self.max_health
        self.max_mana += 10
        self.current_mana = self.max_mana
        
    def rebirth(self):
        # Salva memórias da vida passada
        memory = {
            "level": self.level,
            "class": self.player_class,
            "skills": self.class_skills.copy()
        }
        self.past_life_memories.append(memory)
        
        # Reset para nova vida
        self.rebirth_count += 1
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        self.player_class = None
        self.class_skills = []
        
        # Aplica bônus de renascimento
        bonus_health = min(self.rebirth_count * 10, 50)
        self.max_health = 100 + bonus_health
        self.current_health = self.max_health
        
    def draw(self, screen):
        # Desenha um retângulo simples representando o jogador
        color = (0, 0, 255)  # Azul por padrão
        if self.player_class == PlayerClass.WARRIOR:
            color = (255, 0, 0)  # Vermelho
        elif self.player_class == PlayerClass.MAGE:
            color = (0, 0, 255)  # Azul
        elif self.player_class == PlayerClass.THIEF:
            color = (0, 255, 0)  # Verde
            
        pygame.draw.rect(screen, color, self.rect)

