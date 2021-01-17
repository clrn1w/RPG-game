import pygame
import random
from modules.constants import *
from modules.player import *
from pygame.locals import *
from modules.classes import *
from modules.skill import *
from modules.levels import *


POISON = 1
AMULET = 2
WEAR = 3
ITEMS = 4


class Chest_1_lvl():
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.state = 0
        self.items = []
        self.image = pygame.image.load(r'data/sprites/chests/lvl_1/close.png')
        self.gui = pygame.image.load(r'data/sprites/chests/gui.jpg')
        self.name = 'Chest'
        self.position = [self.x * int(PLAYER_SPEED) + LEFT_MOVE, self.y * int(PLAYER_SPEED)]
        self.hp = 0
        self.item_add()
    
    def item_add(self):
        items = [['Chitaury', AMULET, 100, -20, 0, 0], ['Magic amulet', AMULET, 0, 0, 40, 100], ['Elven Bow', WEAR, 0, 0, 60, 160], ['Heart of Dragon', ITEMS, 20, 150, 0, 0]]
        random_count = random.randint(0, len(items) - 1)
        self.items.append(items[random_count])
    
    def hp_add(self, dmg):
        pass
    
    def render(self, screen):
        if self.state == 0:
            self.image = pygame.image.load(r'data/sprites/chests/lvl_1/close.png')
        else:
            self.image = pygame.image.load(r'data/sprites/chests/lvl_1/open.png')
        self.image = pygame.transform.scale(self.image, (int(PLAYER_SPEED), int(PLAYER_SPEED)))
        screen.blit(self.image, (self.x * int(PLAYER_SPEED) + LEFT_MOVE, self.y * int(PLAYER_SPEED)))

    def render_gui(self, screen):
        self.gui = pygame.transform.scale(self.gui, (500, 500))
        screen.blit(self.gui, (100, 100))


class Chest_2_lvl():
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.state = 0
        self.items = []
        self.image = pygame.image.load(r'data/sprites/chests/lvl_2/close.png')
        self.gui = pygame.image.load(r'data/sprites/chests/gui.jpg')
        self.name = 'Chest'
        self.position = [self.x * int(PLAYER_SPEED) + LEFT_MOVE, self.y * int(PLAYER_SPEED)]
        self.hp = 0
        self.item_add()
    
    def item_add(self):
        items = [['Bow upgrader', ITEMS, 0, 0, 100, 220], ['Health', AMULET, 0, 200, 0, 0], ['Mana upgrader', AMULET, 200, 0, 0, 0], ['Bad poison', POISON, 20, 150, 0, 0]]
        random_count = random.randint(0, len(items) - 1)
        self.items.append(items[random_count])
    
    def hp_add(self, dmg):
        pass
    
    def render(self, screen):
        if self.state == 0:
            self.image = pygame.image.load(r'data/sprites/chests/lvl_2/close.png')
        else:
            self.image = pygame.image.load(r'data/sprites/chests/lvl_2/open.png')
        self.image = pygame.transform.scale(self.image, (int(PLAYER_SPEED), int(PLAYER_SPEED)))
        screen.blit(self.image, (self.x * int(PLAYER_SPEED) + LEFT_MOVE, self.y * int(PLAYER_SPEED)))

    def render_gui(self, screen):
        self.gui = pygame.transform.scale(self.gui, (500, 500))
        screen.blit(self.gui, (100, 100))
