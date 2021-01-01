import pygame
from modules.constants import *
from pygame.locals import *
from modules.classes import *
from modules.skill import *
from modules.chests import * 
from modules.levels import *


class Player():
    def __init__(self, name, game):
        self.direction = LOOK_RIGHT
        self.state = PLAYER_ALIVE
        self.x = START_X + LEFT_MOVE
        self.y = START_Y
        self.name = name
        self.game = game
        self.position = [0, 0]
        self.image = [r'data/sprites/player/player_right_alive.png', r'data/sprites/player/player_right_shoot.png', r'data/sprites/player/player_down_alive.png', r'data/sprites/player/player_down_shoot.png', r'data/sprites/player/player_up_alive.png', r'data/sprites/player/player_up_shoot.png', r'data/sprites/player/player_dead.png']
        self.image = [pygame.image.load(elem) for elem in self.image]
        self.images = []
        self.max_hp = 100
        self.max_mp = 100
        self.hp = 100
        self.mp = 100
        self.attacked = 0
        self.last_sheld = 0
        self.arrow_dmg = 12
        self.fire_arrow_dmg = 120
        self.images.append([[self.image[0], self.image[1], self.image[6]], [self.image[2], self.image[3], self.image[6]], [pygame.transform.flip(self.image[0], True, False), pygame.transform.flip(self.image[1], True, False), self.image[6]], [self.image[4], self.image[5], self.image[6]]])
        self.images = self.images[0]
        self.inventory = []
        self.stoping_hpframe = (LEFT_MOVE + 50 + PLAYER_SPEED // 10) - LEFT_MOVE + 50 + PLAYER_SPEED // 2.4
        self.stoping_mpframe = (LEFT_MOVE + 50 + PLAYER_SPEED // 10) - LEFT_MOVE + 50 + PLAYER_SPEED // 2.4
            
    def move(self, screen, x, y, xd, yd, reburn=False):
        if reburn:
            self.x = START_X + LEFT_MOVE
            self.y = START_Y
            self.position = [0, 0]
            self.player_img = pygame.transform.scale(self.images[self.direction][self.state], (int(PLAYER_SPEED), int(PLAYER_SPEED)))
            screen.blit(self.player_img, (self.x, self.y))
        else:
            if x:
                self.x, self.y = self.x + PLAYER_SPEED, self.y
                screen.blit(self.images[self.direction][self.state], (self.x, self.y))
            elif y:
                self.x, self.y = self.x, self.y + PLAYER_SPEED
                screen.blit(self.images[self.direction][self.state], (self.x, self.y))
            elif xd:
                self.x, self.y = self.x - PLAYER_SPEED, self.y
                screen.blit(self.images[self.direction][self.state], (self.x, self.y))
            elif yd:
                self.x, self.y = self.x, self.y - PLAYER_SPEED
                screen.blit(self.images[self.direction][self.state], (self.x, self.y))
        
    def render(self, screen):
        self.check_die()
        self.player_img = pygame.transform.scale(self.images[self.direction][self.state], (int(PLAYER_SPEED), int(PLAYER_SPEED)))
        screen.blit(self.player_img, (self.x, self.y))

    def render_ui(self, screen):
        if self.state != PLAYER_DEAD and self.hp <= self.max_hp:
            if self.max_hp < 0:
                self.hptick = (self.stoping_hpframe / self.max_hp)
            else:
                self.hptick = (self.max_hp / self.stoping_hpframe)
            pygame.draw.rect(screen, pygame.Color('red'), (LEFT_MOVE + 50, SCREEN_HEIGHT - 100, self.hp // self.hptick, 20))
        else:
            pygame.draw.rect(screen, pygame.Color('red'), (LEFT_MOVE + 50, SCREEN_HEIGHT - 100, self.stoping_hpframe, 20))

    def render_mp(self, screen):
        if self.state != PLAYER_DEAD and self.mp <= self.max_mp:
            self.mptick = (self.max_mp / self.stoping_mpframe)
            pygame.draw.rect(screen, pygame.Color('blue'), (LEFT_MOVE + 50, SCREEN_HEIGHT - 50, self.mp // self.mptick, 20))
        else:
            pygame.draw.rect(screen, pygame.Color('blue'), (LEFT_MOVE + 50, SCREEN_HEIGHT - 50, self.stoping_mpframe, 20))

    def contact_check(self, obj):
        res = False
        for el in obj:
            if el.name in ['Ork', 'Dragon']:
                el_x, el_y = el.position[0], el.position[1]
            else:
                el_x, el_y = el.x, el.y
            if self.direction == LOOK_RIGHT:
                if self.position[0] == el_x and self.position[1] == el_y:
                    return True
                else:
                    res = False
            elif self.direction == LOOK_DOWN:
                if self.position[0] == el_x and self.position[1] == el_y:
                    return True
                else:
                    res = False 
            elif self.direction == LOOK_LEFT:
                if self.position[0] == el_x and self.position[1] == el_y:
                    return True
                else:
                    res = False
            elif self.direction == LOOK_UP:
                if self.position[0] == el_x and self.position[1] == el_y:
                    return True
                else:
                    res = False
        return res
    
    def check_die(self):
        if self.hp <= 0 and self.state != PLAYER_DEAD:
            self.state = PLAYER_DEAD
            self.game.play_music(PLAYER_DEATH_MUSIC)
            pygame.mixer.music.pause()

    def hp_add(self, dmg):
        self.hp += dmg
        if self.hp <= 0:
            self.check_die()


  
  
  
