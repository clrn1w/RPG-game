import pygame
import random
from modules.constants import *
from modules.player import *
from pygame.locals import *
from modules.classes import *
from modules.chests import * 
from modules.levels import *

class Fireball():
    def __init__(self, screen,game, x, y, direction, position, dmg, owner):
        self.direction = direction
        self.game = game
        self.owner = owner
        self.cd = 10
        self.count = FIRE_ARROW_COUNT
        self.speed = 20
        self.images = []
        for i in range(4):
            if i == 0:
                self.images.append(pygame.transform.rotate(pygame.image.load(r'data/sprites/mobs/dragon_green/fireball.png'), 180))
            elif i == 1:
                self.images.append(pygame.transform.rotate(pygame.image.load(r'data/sprites/mobs/dragon_green/fireball.png'), 90))
            elif i == 2:
                self.images.append(pygame.image.load(r'data/sprites/mobs/dragon_green/fireball.png'))
            elif i == 3:
                self.images.append(pygame.transform.rotate(pygame.image.load(r'data/sprites/mobs/dragon_green/fireball.png'), 270))
        self.position = position
        self.x = x
        self.y = y
        self.damage = 45

    def render(self, screen):
        if self.direction in [LOOK_LEFT, LOOK_RIGHT]:
            self.arrow_img = pygame.transform.scale(self.images[self.direction], (SCREEN_WIDTH // 100, SCREEN_HEIGHT // 100))
        else:
            self.arrow_img = pygame.transform.scale(self.images[self.direction], (SCREEN_HEIGHT // 100, SCREEN_WIDTH // 100))
        screen.blit(self.arrow_img, (self.x, self.y))

    def move(self):
        if self.direction == LOOK_RIGHT:
            self.x += self.speed
        elif self.direction == LOOK_DOWN:
            self.y += self.speed
        elif self.direction == LOOK_LEFT:
            self.x -= self.speed
        elif self.direction == LOOK_UP:
            self.y -= self.speed
        if self.contact_check(self.game.obj):
            self.remove()
        if self.x <= LEFT_MOVE or self.x >= LEFT_MOVE + PLAYER_SPEED * 22 or self.y <= (0) or self.y >= (PLAYER_SPEED * 16 - PLAYER_SPEED*0.2):
                self.remove()
    
    def contact_check(self, obj):
        arrow_x, arrow_y = (self.x - LEFT_MOVE) // PLAYER_SPEED, (self.y - PLAYER_SPEED // 2) // PLAYER_SPEED
        for el in obj:
            if True:
                if el == self.game.player:
                    el_x, el_y = el.position[0], el.position[1]
                    if self.direction != LOOK_UP:
                        if arrow_x == el_x and arrow_y == el_y:
                            if el == self.game.player and el in self.game.shelding:
                                el.hp_add(dmg=-int(self.damage * 0.4))
                                if el.hp >0:
                                    self.game.play_music(SHELD)
                                    pygame.mixer.music.stop()
                            else:
                                el.hp_add(dmg=-int(self.damage))
                                if el.hp >0:
                                    self.game.play_music(PLAYER_KICK_MUSIC)
                                    pygame.mixer.music.stop()
                            self.remove()
                    else:
                        if arrow_x == el_x and arrow_y + 1 == el_y:
                            if el == self.game.player and el in self.game.shelding:
                                el.hp_add(dmg=-int(self.damage * 0.4))
                                if el.hp >0:
                                    self.game.play_music(SHELD)
                                    pygame.mixer.music.stop()
                            else:
                                el.hp_add(dmg=-int(self.damage))
                                if el.hp >0:
                                    self.game.play_music(PLAYER_KICK_MUSIC)
                                    pygame.mixer.music.stop()
                            self.remove()
                elif el.name == 'Ork':
                    el_x, el_y = el.position[0], el.position[1]
                    if self.direction != LOOK_UP:
                        if arrow_x == el_x and arrow_y == el_y:
                            if el == self.game.player and el in self.game.shelding:
                                self.game.play_music(SHELD)
                                pygame.mixer.music.stop()
                            else:
                                el.hp_add(dmg=-int(self.damage))
                                if el.hp >0:
                                    self.game.play_music(el.musik_kick)
                                    pygame.mixer.music.stop()
                            self.remove()
                    else:
                        if arrow_x == el_x and arrow_y + 1 == el_y:
                            if el == self.game.player and el in self.game.shelding:
                                self.game.play_music(SHELD)
                                pygame.mixer.music.stop()
                            else:
                                el.hp_add(dmg=-int(self.damage))
                                if el.hp >0:
                                    el.musik_kick.play()
                                    pygame.mixer.music.stop()
                            self.remove()
                elif el.name == 'Stone_1':
                    el_x, el_y = (el.position[0] - LEFT_MOVE) // PLAYER_SPEED, el.position[1] // PLAYER_SPEED
                    if self.direction != LOOK_UP:
                        if arrow_x == el_x and arrow_y == el_y:
                            el.hp_add(dmg=-int(self.damage))
                            if el.hp >0:
                                self.game.play_music(STONE1_KICK_MUSIC)
                                pygame.mixer.music.stop()
                            self.remove()
                    else:
                        if arrow_x == el_x and arrow_y + 1 == el_y:
                            el.hp_add(dmg=-int(self.damage))
                            if el.hp >0:
                                self.game.play_music(STONE1_KICK_MUSIC)
                                pygame.mixer.music.stop()
                            self.remove()
                else:
                    el_x, el_y = (el.position[0] - LEFT_MOVE) // PLAYER_SPEED, el.position[1] // PLAYER_SPEED
                    if self.direction != LOOK_UP:
                        if arrow_x == el_x and arrow_y == el_y:
                            el.hp_add(dmg=-int(self.damage))
                            self.remove()
                    else:
                        if arrow_x == el_x and arrow_y + 1 == el_y:
                            el.hp_add(dmg=-int(self.damage))
                            self.remove()

    def remove(self):
        if self in self.game.projective:
            self.game.projective.remove(self)


class Fire_arrow():
    def __init__(self, screen,game, x, y, direction, position, dmg, owner):
        self.direction = direction
        self.game = game
        self.owner = owner
        self.cd = 10
        self.count = FIRE_ARROW_COUNT
        self.speed = 50
        self.images = [r'data/sprites/arrow/arrow_right_fire.png', r'data/sprites/arrow/arrow_down_fire.png', r'data/sprites/arrow/arrow_left_fire.png', r'data/sprites/arrow/arrow_up_fire.png']
        self.images = [pygame.image.load(elem) for elem in self.images]
        self.position = position
        self.x = x
        self.y = y
        self.damage = dmg

    def render(self, screen):
        if self.direction in [LOOK_LEFT, LOOK_RIGHT]:
            self.arrow_img = pygame.transform.scale(self.images[self.direction], (SCREEN_WIDTH // 100, SCREEN_HEIGHT // 100))
        else:
            self.arrow_img = pygame.transform.scale(self.images[self.direction], (SCREEN_HEIGHT // 100, SCREEN_WIDTH // 100))
        screen.blit(self.arrow_img, (self.x, self.y))

    def move(self):
        if self.direction == LOOK_RIGHT:
            self.x += self.speed
        elif self.direction == LOOK_DOWN:
            self.y += self.speed
        elif self.direction == LOOK_LEFT:
            self.x -= self.speed
        elif self.direction == LOOK_UP:
            self.y -= self.speed
        if self.contact_check(self.game.obj):
            self.remove()
        if self.x <= LEFT_MOVE or self.x >= LEFT_MOVE + PLAYER_SPEED * 22 or self.y <= (0) or self.y >= (PLAYER_SPEED * 16 - PLAYER_SPEED*0.2):
                self.remove()
    
    def contact_check(self, obj):
        arrow_x, arrow_y = (self.x - LEFT_MOVE) // PLAYER_SPEED, (self.y - PLAYER_SPEED // 2) // PLAYER_SPEED
        for el in obj:
            if True:
                if el.name in ['Ork', 'Dragon']:
                    el_x, el_y = el.position[0], el.position[1]
                    if self.direction != LOOK_UP:
                        if arrow_x == el_x and arrow_y == el_y:
                            if el in self.game.shelding:
                                self.game.play_music(SHELD)
                            else:
                                el.hp_add(dmg=-int(self.damage))
                                if el.hp >0:
                                    self.game.play_music(el.musik_kick)
                                    pygame.mixer.music.stop()
                                print('damaged')
                            self.remove()
                    else:
                        if arrow_x == el_x and arrow_y + 1 == el_y:
                            if el in self.game.shelding:
                                self.game.play_music(SHELD)
                            else:
                                el.hp_add(dmg=-int(self.damage))
                                if el.hp >0:
                                    self.game.play_music(el.musik_kick)
                                    pygame.mixer.music.stop()
                            self.remove()
                elif el.name == 'Stone_1':
                    el_x, el_y = (el.position[0] - LEFT_MOVE) // PLAYER_SPEED, el.position[1] // PLAYER_SPEED
                    if self.direction != LOOK_UP:
                        if arrow_x == el_x and arrow_y == el_y:
                            el.hp_add(dmg=-int(self.damage))
                            if el.hp >0:
                                self.game.play_music(STONE1_KICK_MUSIC)
                            self.remove()
                    else:
                        if arrow_x == el_x and arrow_y + 1 == el_y:
                            el.hp_add(dmg=-int(self.damage))
                            if el.hp >0:
                                self.game.play_music(STONE1_KICK_MUSIC)
                            self.remove()
                else:
                    el_x, el_y = (el.position[0] - LEFT_MOVE) // PLAYER_SPEED, el.position[1] // PLAYER_SPEED
                    if self.direction != LOOK_UP:
                        if arrow_x == el_x and arrow_y == el_y:
                            if el in self.game.shelding:
                                self.game.play_music(SHELD)
                                pygame.mixer.music.stop()
                            else:
                                el.hp_add(dmg=-int(self.damage))
                            self.remove()
                    else:
                        if arrow_x == el_x and arrow_y + 1 == el_y:
                            if el in self.game.shelding:
                                self.game.play_music(SHELD)
                                pygame.mixer.music.stop()
                            else:
                                el.hp_add(dmg=-int(self.damage))
                            self.remove()
            else:
                print('blocked')

    def remove(self):
        if self in self.game.projective:
            self.game.projective.remove(self)


class Sheld():
    def __init__(self, screen, game, owner):
        self.timer = 100
        self.conut = 40
        self.cd = 300
        self.image = pygame.image.load(r'data/sprites/player/Sheld.png')
        self.owner = owner
        self.screen = screen
        self.game = game
    
    def render(self, screen):
        if self.owner == self.game.player:
            self.image = pygame.transform.scale(self.image, (PLAYER_SPEED, PLAYER_SPEED))
            self.screen.blit(self.image, (self.owner.x, self.owner.y))
        else:
            self.image = pygame.transform.scale(self.image, (PLAYER_SPEED, PLAYER_SPEED))
            self.screen.blit(self.image, (self.owner.position[0], self.owner.position[1]))
    
    def remove(self):
        if self in self.game.shelding:
            self.game.shelding.remove(self)