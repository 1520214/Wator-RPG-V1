import pygame
from enum import Enum

class GameState(Enum):
    MENU = "menu"
    CLASS_SELECTION = "class_selection"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    REBIRTH = "rebirth"

class GameStateManager:
    def __init__(self):
        self.current_state = GameState.MENU
        self.previous_state = None
        
    def change_state(self, new_state):
        self.previous_state = self.current_state
        self.current_state = new_state
        
    def get_current_state(self):
        return self.current_state
        
    def get_previous_state(self):
        return self.previous_state

