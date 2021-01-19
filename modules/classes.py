import pygame
from modules.constants import *
from modules.player import *
from pygame.locals import *
from modules.skill import *
from modules.chests import * 
from modules.levels import *

class Arrow():
    def __init__(self, screen,game, x, y, direction, position, dmg):
        self.direction = direction
        self.game = game
        self.speed = 15
        self.images = [r'data/sprites/arrow/arrow_right.png', r'data/sprites/arrow/arrow_down.png', r'data/sprites/arrow/arrow_left.png', r'data/sprites/arrow/arrow_up.png']
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
            if el != self.game.player:
                if el.name in ['Ork', 'Dragon']:
                    el_x, el_y = el.position[0], el.position[1]
                    if self.direction != LOOK_UP:
                        if arrow_x == el_x and arrow_y == el_y:
                            el.hp_add(dmg=-int(self.damage))
                            if el.hp >0:
                                self.game.play_music(el.musik_kick)
                            self.remove()
                    else:
                        if arrow_x == el_x and arrow_y + 1 == el_y:
                            el.hp_add(dmg=-int(self.damage))
                            if el.hp >0:
                                self.game.play_music(el.musik_kick)
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
                            el.hp_add(dmg=-int(self.damage))
                            self.remove()
                    else:
                        if arrow_x == el_x and arrow_y + 1 == el_y:
                            el.hp_add(dmg=-int(self.damage))
                            self.remove()


    def remove(self):
        if self in self.game.projective:
            self.game.projective.remove(self)


class Stone():
    def __init__(self, screen, game, x, y):
        self.image = pygame.image.load(r'data/sprites/stone_1.png')
        self.killed_image = pygame.image.load(r'data/sprites/broken_stone_1.png')
        self.x = x - 1
        self.y = y - 1
        self.game = game
        self.name = 'Stone_1'
        self.state = PLAYER_ALIVE
        self.position = [self.x * int(PLAYER_SPEED) + LEFT_MOVE, self.y * int(PLAYER_SPEED)]
        self.hp = 12000
    
    def render(self, screen):
        if self.state == PLAYER_ALIVE:
            self.image = pygame.transform.scale(self.image, (int(PLAYER_SPEED), int(PLAYER_SPEED)))
            screen.blit(self.image, (self.x * int(PLAYER_SPEED) + LEFT_MOVE, self.y * int(PLAYER_SPEED)))
        else:
            self.image = pygame.transform.scale(self.killed_image, (int(PLAYER_SPEED), int(PLAYER_SPEED)))
            screen.blit(self.image, (self.x * int(PLAYER_SPEED) + LEFT_MOVE, self.y * int(PLAYER_SPEED)))

    def hp_add(self, dmg):
        self.hp += dmg
        if self.hp <= 0:
            self.kill()
    
    def kill(self):
        if self in self.game.obj:
            self.state = PLAYER_DEAD
            self.game.obj.remove(self)
            self.game.killed_obj.append(self)
            STONE1_DEATH_MUSIC.play()
            pygame.mixer.music.stop()


class Tnt():
    def __init__(self, screen, game, x, y):
        self.image = pygame.image.load(r'data/sprites/tnt.png')
        self.killed_image = pygame.image.load(r'data/sprites/boom.png')
        self.x = x - 1
        self.y = y - 1
        self.game = game
        self.name = 'TNT'
        self.state = PLAYER_ALIVE
        self.position = [self.x * int(PLAYER_SPEED) + LEFT_MOVE, self.y * int(PLAYER_SPEED)]
        self.hp = 1
    
    def render(self, screen):
        if self.state == PLAYER_ALIVE:
            self.image = pygame.transform.scale(self.image, (int(PLAYER_SPEED), int(PLAYER_SPEED)))
            screen.blit(self.image, (self.x * int(PLAYER_SPEED) + LEFT_MOVE, self.y * int(PLAYER_SPEED)))
        else:
            self.image = pygame.transform.scale(self.killed_image, (int(PLAYER_SPEED), int(PLAYER_SPEED)))
            screen.blit(self.image, (self.x * int(PLAYER_SPEED) + LEFT_MOVE, self.y * int(PLAYER_SPEED)))

    def hp_add(self, dmg):
        self.hp += dmg
        if self.hp <= 0:
            self.kill()
    
    def kill(self):
        if self in self.game.obj:
            x,y = self.x, self.y
            destroy_pos = [[x, y - 1], [x + 1, y - 1], [x + 1, y], [x + 1, y + 1], [x, y + 1], [x - 1, y + 1], [x - 1, y], [x - 1, y - 1]]
            for el in self.game.obj:
            	if el.name == 'stone_1':
            		position = [el.x, el.y]
            	else:
            		position = [el.position[0], el.position[1]]
            	if position in destroy_pos:
            		el.hp_add(-9999)
            	if self.game.player.position in destroy_pos:
            		self.game.player.hp -= 99999
            self.state = PLAYER_DEAD
            self.game.obj.remove(self)
            self.game.killed_obj.append(self)
            self.game.killed_obj.remove(self)
            self.game.play_music(BOOM)
            pygame.mixer.music.stop()


class Mob_ork():
    def __init__(self, name, game, x, y):
        self.clock_attack = -1
        self.direction = LOOK_RIGHT
        self.state = PLAYER_ALIVE
        self.x = x - 1
        self.y = y - 1
        self.musik_kick = ORK_KICK_MUSIC
        self.musik_deth = ORK_DEATH_MUSIC
        self.x, self.y = self.x * int(PLAYER_SPEED) + LEFT_MOVE, self.y * int(PLAYER_SPEED)
        self.name = name
        self.position = [x - 1, y - 1]
        self.game = game
        self.image = [r'data/sprites/mobs/ork/ork_right_alive.png', r'data/sprites/mobs/ork/ork_right_shoot.png', r'data/sprites/mobs/ork/ork_down_alive.png', r'data/sprites/mobs/ork/ork_down_shoot.png', r'data/sprites/mobs/ork/ork_up_alive.png', r'data/sprites/mobs/ork/ork_up_shoot.png', r'data/sprites/mobs/ork/ork_dead.png']
        self.image = [pygame.image.load(elem) for elem in self.image]
        self.images = []
        self.hp = MAX_HP
        self.mp = MAX_MP
        self.damage = 40
        self.player = self.game.player
        self.images.append([[self.image[0], self.image[1], self.image[6]], [self.image[2], self.image[3], self.image[6]], [pygame.transform.flip(self.image[0], True, False), pygame.transform.flip(self.image[1], True, False), self.image[6]], [self.image[4], self.image[5], self.image[6]]])
        self.images = self.images[0]
        self.stop = 0
        self.stoping_hpframe = (self.x + PLAYER_SPEED // 10) - self.x + PLAYER_SPEED // 2.4
        if self.hp >= self.stoping_hpframe:
            self.hptick = (self.hp / self.stoping_hpframe)
        else:
            self.hptick = (self.stoping_hpframe / self.hp)
  
    def move(self, screen, x, y, xd, yd, reburn=False):
        if self.game.game_stop == 0:
            if reburn:
                self.x = START_X + LEFT_MOVE
                self.y = START_Y
                self.position = [0, 0]
                self.player_img = pygame.transform.scale(self.images[self.direction][self.state], (int(PLAYER_SPEED), int(PLAYER_SPEED)))
                screen.blit(self.player_img, (self.x, self.y))
            else:
                if True:
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
        self.player_img = pygame.transform.scale(self.images[self.direction][self.state], (int(PLAYER_SPEED), int(PLAYER_SPEED)))
        screen.blit(self.player_img, (self.x, self.y))
    
    def render_ui(self, screen):
        img = pygame.transform.scale(pygame.image.load(r'data/sprites/mobs/hpframe.png'), (int(PLAYER_SPEED / 1.5), int(PLAYER_SPEED / 1.5)))
        screen.blit(img, (int(self.x + PLAYER_SPEED // 4), int(self.y + PLAYER_SPEED // 2)))
        pygame.draw.rect(screen, (255, 0, 0), (self.x + PLAYER_SPEED // 2.4, self.y + PLAYER_SPEED // 1.35, self.hp // self.hptick, int(PLAYER_SPEED / 1.5) // 6))

    def hp_add(self, dmg):
        self.hp += dmg
        if self.hp <= 0:
            self.kill()
    
    def kill(self):
        if self in self.game.obj:
            self.state = PLAYER_DEAD
            self.game.obj.remove(self)
            if self.attack_1():
                self.stop = 1
                self.game.player.attacked = 1
            else:
                self.stop = 0
            self.game.player.attacked = 0
            self.game.killed_mobs.append(self)
            self.game.play_music(self.musik_deth)

    def contact_check(self, obj):
        res = False
        for el in obj:
            if el.name == 'Ork' and el != self:
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
                if self.position[0] == el_x and self.position[1]  == el_y:
                    return True
                else:
                    res = False
        if self.direction == LOOK_RIGHT:
            if self.position[0] == self.player.position[0] and self.position[1] == self.player.position[1]:
                return True
            else:
                res = False
        elif self.direction == LOOK_DOWN:
            if self.position[0] == self.player.position[0] and self.position[1] == self.player.position[1]:
                return True
            else:
                res = False 
        elif self.direction == LOOK_LEFT:
            if self.position[0] == self.player.position[0] and self.position[1] == self.player.position[1]:
                return True
            else:
                res = False
        elif self.direction == LOOK_UP:
            if self.position[0] == self.player.position[0] and self.position[1]  == self.player.position[1]:
                return True
            else:
                res = False
        return res

    def random_move(self, screen):
        if self.game.game_stop == 0:
            move = random.randint(0, 3)
            obj = self.game.obj
            x,y,xd,yd = False, False, False, False
            self.attack()
            if self.stop == 0 and self.state != PLAYER_SHOOT:
                if move == 0:
                    self.direction = LOOK_UP
                    self.position[1] -= 1
                    if self.position[1] > 15 or self.position[1] < 0 or self.contact_check(obj):
                        self.position[1] += 1
                    else:
                        yd = True
                        self.move(screen, x, y, xd, yd)
                elif move == 1:
                    self.direction = LOOK_DOWN
                    self.position[1] += 1
                    if self.position[1] > 15 or self.position[1] < 0 or self.contact_check(obj):
                        self.position[1] -= 1
                    else:
                        y = True
                        self.move(screen, x, y, xd, yd)
                elif move == 2:
                    self.direction = LOOK_RIGHT
                    self.position[0] += 1
                    if self.position[0] > 21 or self.position[0] < 0 or self.contact_check(obj):
                        self.position[0] -= 1
                    else:
                        x = True
                        self.move(screen, x, y, xd, yd)
                elif move == 3:
                    self.direction = LOOK_LEFT
                    self.position[0] -= 1
                    if self.position[0] > 21 or self.position[0] < 0 or self.contact_check(obj):
                        self.position[0] += 1
                    else:
                        xd = True
                        self.move(screen, x, y, xd, yd)
    
    def attack(self):
        if self.game.game_stop == 0:
            if self.game.player.state != PLAYER_DEAD:
                pos_ork_x, pos_ork_y, pos_p_x, pos_p_y = self.position[0], self.position[1], self.game.player.position[0], self.game.player.position[1]
                res = False
                if pos_ork_x - 1 == pos_p_x and pos_ork_y == pos_p_y:
                    self.direction = LOOK_LEFT
                    if self.game.player in self.game.shelding:
                        self.game.play_music(SHELD)
                    else:
                        self.game.player.hp -= self.damage
                    res = True
                elif pos_ork_x + 1 == pos_p_x and pos_ork_y == pos_p_y:
                    self.direction = LOOK_RIGHT
                    if self.game.player in self.game.shelding:
                        self.game.play_music(SHELD)
                    else:
                        self.game.player.hp -= self.damage
                    res = True
                elif pos_ork_x  == pos_p_x and pos_ork_y - 1 == pos_p_y:
                    self.direction = LOOK_UP
                    if self.game.player in self.game.shelding:
                        self.game.play_music(SHELD)
                    else:
                        self.game.player.hp -= self.damage
                    res = True
                elif pos_ork_x == pos_p_x and pos_ork_y + 1== pos_p_y:
                    self.direction = LOOK_DOWN
                    if self.game.player in self.game.shelding:
                        self.game.play_music(SHELD)
                    else:
                        self.game.player.hp -= self.damage
                    res = True
                if self.attack_1():
                    self.state = PLAYER_SHOOT
                    self.stop = 1
                    self.game.player.attacked = 1
                    if self.game.player not in self.game.shelding:
                        if self.game.player.hp > 0:
                            self.game.play_music(PLAYER_KICK_MUSIC)
                elif not self.attack_1() and self.stop == 1:
                    self.state = PLAYER_ALIVE
                    self.stop = 0
                    self.game.player.attacked = 0

            else:
                self.state = PLAYER_ALIVE
                self.stop = 0
    
    def attack_1(self):
        pos_ork_x, pos_ork_y, pos_p_x, pos_p_y = self.position[0], self.position[1], self.game.player.position[0], self.game.player.position[1]
        res = False
        if pos_ork_x - 1 == pos_p_x and pos_ork_y == pos_p_y:
            res = True
        elif pos_ork_x + 1 == pos_p_x and pos_ork_y == pos_p_y:
            res = True
        elif pos_ork_x == pos_p_x and pos_ork_y - 1 == pos_p_y:
            res = True
        elif pos_ork_x == pos_p_x and pos_ork_y + 1== pos_p_y:
            res = True
        return res


class Mob_dragon():
    def __init__(self, name, game, x, y, screen):
        self.clock_attack = -1
        self.screen = screen
        self.direction = LOOK_RIGHT
        self.state = PLAYER_ALIVE
        self.x = x - 1
        self.y = y - 1
        self.musik_kick = DRAGON_KICK_MUSIC
        self.musik_deth = DRAGON_DEATH_MUSIC
        self.x, self.y = self.x * int(PLAYER_SPEED) + LEFT_MOVE, self.y * int(PLAYER_SPEED)
        self.name = 'Dragon'
        self.cell_size = PLAYER_SPEED
        self.position = [x - 1, y - 1]
        self.game = game
        self.image = [r'data/sprites/mobs/dragon_green/r_a.png', r'data/sprites/mobs/dragon_green/r_s.png', r'data/sprites/mobs/dragon_green/d_a.png', r'data/sprites/mobs/dragon_green/d_s.png', r'data/sprites/mobs/dragon_green/u_a.png', r'data/sprites/mobs/dragon_green/u_s.png', r'data/sprites/mobs/dragon_green/dead.png']
        self.image = [pygame.image.load(elem) for elem in self.image]
        self.images = []
        self.hp = 1600
        self.mp = MAX_MP
        self.damage = 99
        self.player = self.game.player
        self.images.append([[self.image[0], self.image[1], self.image[6]], [self.image[2], self.image[3], self.image[6]], [pygame.transform.flip(self.image[0], True, False), pygame.transform.flip(self.image[1], True, False), self.image[6]], [self.image[4], self.image[5], self.image[6]]])
        self.images = self.images[0]
        self.stop = 0
        self.stoping_hpframe = (self.x + PLAYER_SPEED // 10) - self.x + PLAYER_SPEED // 2.4
        if self.hp >= self.stoping_hpframe:
            self.hptick = (self.hp / self.stoping_hpframe)
        else:
            self.hptick = (self.stoping_hpframe / self.hp)
            
    def move(self, screen, x, y, xd, yd, reburn=False):
        if self.game.game_stop == 0:
            if reburn:
                self.x = START_X + LEFT_MOVE
                self.y = START_Y
                self.position = [0, 0]
                self.player_img = pygame.transform.scale(self.images[self.direction][self.state], (int(PLAYER_SPEED), int(PLAYER_SPEED)))
                screen.blit(self.player_img, (self.x, self.y))
            else:
                if True:
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
        self.player_img = pygame.transform.scale(self.images[self.direction][self.state], (int(PLAYER_SPEED), int(PLAYER_SPEED)))
        screen.blit(self.player_img, (self.x, self.y))
    
    def render_ui(self, screen):
        img = pygame.transform.scale(pygame.image.load(r'data/sprites/mobs/hpframe.png'), (int(PLAYER_SPEED / 1.5), int(PLAYER_SPEED / 1.5)))
        screen.blit(img, (int(self.x + PLAYER_SPEED // 4), int(self.y + PLAYER_SPEED // 2)))
        pygame.draw.rect(screen, (255, 0, 0), (self.x + PLAYER_SPEED // 2.2, self.y + PLAYER_SPEED // 1.35, self.hp // self.hptick, int(PLAYER_SPEED / 1.5) // 6))

    def hp_add(self, dmg):
        self.hp += dmg
        if self.hp <= 0:
            self.kill()
    
    def kill(self):
        if self in self.game.obj:
            self.state = PLAYER_DEAD
            self.game.obj.remove(self)
            if self.attack_1():
                self.stop = 1
                self.game.player.attacked = 1
            else:
                self.stop = 0
                self.game.player.attacked = 0
            self.game.player.attacked = 0
            self.game.killed_mobs.append(self)
            self.game.play_music(self.musik_deth)


    def contact_check(self, obj):
        res = False
        for el in obj:
            if el.name == 'Ork' and el != self:
                el_x, el_y = el.position[0], el.position[1]
            if el.name == 'Dragon' and el != self:
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
                if self.position[0] == el_x and self.position[1]  == el_y:
                    return True
                else:
                    res = False
        if self.direction == LOOK_RIGHT:
            if self.position[0] == self.player.position[0] and self.position[1] == self.player.position[1]:
                return True
            else:
                res = False
        elif self.direction == LOOK_DOWN:
            if self.position[0] == self.player.position[0] and self.position[1] == self.player.position[1]:
                return True
            else:
                res = False 
        elif self.direction == LOOK_LEFT:
            if self.position[0] == self.player.position[0] and self.position[1] == self.player.position[1]:
                return True
            else:
                res = False
        elif self.direction == LOOK_UP:
            if self.position[0] == self.player.position[0] and self.position[1]  == self.player.position[1]:
                return True
            else:
                res = False
        return res

    def random_move(self, screen):
        if self.game.game_stop == 0:
            move = random.randint(0, 3)
            obj = self.game.obj
            x,y,xd,yd = False, False, False, False
            self.attack()
            if self.stop == 0 and self.state != PLAYER_SHOOT:
                if move == 0:
                    self.direction = LOOK_UP
                    self.position[1] -= 1
                    if self.position[1] > 15 or self.position[1] < 0 or self.contact_check(obj):
                        self.position[1] += 1
                    else:
                        yd = True
                        self.move(screen, x, y, xd, yd)
                elif move == 1:
                    self.direction = LOOK_DOWN
                    self.position[1] += 1
                    if self.position[1] > 15 or self.position[1] < 0 or self.contact_check(obj):
                        self.position[1] -= 1
                    else:
                        y = True
                        self.move(screen, x, y, xd, yd)
                elif move == 2:
                    self.direction = LOOK_RIGHT
                    self.position[0] += 1
                    if self.position[0] > 21 or self.position[0] < 0 or self.contact_check(obj):
                        self.position[0] -= 1
                    else:
                        x = True
                        self.move(screen, x, y, xd, yd)
                elif move == 3:
                    self.direction = LOOK_LEFT
                    self.position[0] -= 1
                    if self.position[0] > 21 or self.position[0] < 0 or self.contact_check(obj):
                        self.position[0] += 1
                    else:
                        xd = True
                        self.move(screen, x, y, xd, yd)
    
    def attack(self):
        if self.game.game_stop == 0:
            if self.game.player.state != PLAYER_DEAD:
                res = False
                pos = self.position
                x,y = self.position[0], self.position[1]
                if self.game.player.position in [[x-1, y], [x-2, y], [x-3, y], [x-4, y], [x-5, y], [x-6, y], [x-7, y]]:
                    self.direction = LOOK_LEFT
                    self.game.projective.append(Fireball(screen=self.screen, x=self.x + 7, y=self.y + self.cell_size//2, direction=self.direction, game=self.game, position=pos, dmg=6000, owner=self))
                    res = True
                elif self.game.player.position in [[x+1, y], [x+2, y], [x+3, y], [x+4, y], [x+5, y], [x+6, y], [x+7, y]]:
                    self.direction = LOOK_RIGHT
                    self.game.projective.append(Fireball(screen=self.screen, x=self.x + 7, y=self.y + self.cell_size // 2, direction=self.direction, game=self.game, position=pos, dmg=6000, owner=self))
                    res = True
                elif self.game.player.position in [[x, y-1], [x, y-2], [x, y-3], [x, y-4], [x, y-5], [x, y-6], [x, y-7]]:
                    self.direction = LOOK_UP
                    self.game.projective.append(Fireball(screen=self.screen, x=self.x + self.cell_size // 2 - 4, y=self.y - 7, direction=self.direction, game=self.game, position=pos, dmg=6000, owner=self))
                    res = True
                elif self.game.player.position in [[x, y+1], [x, y+2], [x, y+3], [x, y+4], [x, y+5], [x, y+6], [x, y+7]]:
                    self.direction = LOOK_DOWN
                    self.game.projective.append(Fireball(screen=self.screen, x=self.x + self.cell_size // 2 - 4, y=self.y + 7, direction=self.direction, game=self.game, position=pos, dmg=6000, owner=self))
                    res = True
                if self.attack_1():
                    self.state = PLAYER_SHOOT
                    self.stop = 1
                elif not self.attack_1() and self.stop == 1:
                    self.state = PLAYER_ALIVE
                    self.stop = 0
            else:
                self.state = PLAYER_ALIVE
                self.stop = 0
    
    def attack_1(self):
        res = False
        x, y = self.position[0], self.position[1]
        if self.game.player.position in [[x-1, y], [x-2, y], [x-3, y], [x-4, y], [x-5, y], [x-6, y], [x-7, y]]:
            res = True
        elif self.game.player.position in [[x+1, y], [x+2, y], [x+3, y], [x+4, y], [x+5, y], [x+6, y], [x+7, y]]:
            res = True
        elif self.game.player.position in [[x, y-1], [x, y-2], [x, y-3], [x, y-4], [x, y-5], [x, y-6], [x, y-7]]:
            res = True
        elif self.game.player.position in [[x, y+1], [x, y+2], [x, y+3], [x, y+4], [x, y+5], [x, y+6], [x, y+7]]:
            res = True
        return res


class Mob_ork_boss():
    def __init__(self, name, game, x, y):
        self.clock_attack = -1
        self.direction = LOOK_RIGHT
        self.state = PLAYER_ALIVE
        self.x = x - 1
        self.y = y - 1
        self.musik_kick = ORK_KICK_MUSIC
        self.musik_deth = ORK_DEATH_MUSIC
        self.x, self.y = self.x * int(PLAYER_SPEED) + LEFT_MOVE, self.y * int(PLAYER_SPEED)
        self.name = name
        self.position = [x - 1, y - 1]
        self.game = game
        self.image = [r'data/sprites/mobs/ork_boss/ork_right_alive.png', r'data/sprites/mobs/ork_boss/ork_right_shoot.png', r'data/sprites/mobs/ork_boss/ork_down_alive.png', r'data/sprites/mobs/ork_boss/ork_down_shoot.png', r'data/sprites/mobs/ork_boss/ork_up_alive.png', r'data/sprites/mobs/ork_boss/ork_up_shoot.png', r'data/sprites/mobs/ork_boss/ork_dead.png']
        self.image = [pygame.image.load(elem) for elem in self.image]
        self.images = []
        self.hp = 1000
        self.mp = MAX_MP
        self.damage = 99
        self.player = self.game.player
        self.images.append([[self.image[0], self.image[1], self.image[6]], [self.image[2], self.image[3], self.image[6]], [pygame.transform.flip(self.image[0], True, False), pygame.transform.flip(self.image[1], True, False), self.image[6]], [self.image[4], self.image[5], self.image[6]]])
        self.images = self.images[0]
        self.stop = 0
        self.stoping_hpframe = (self.x + PLAYER_SPEED // 10) - self.x + PLAYER_SPEED // 2.4
        if self.hp >= self.stoping_hpframe:
            self.hptick = (self.hp / self.stoping_hpframe)
        else:
            self.hptick = (self.stoping_hpframe / self.hp)
              
    def move(self, screen, x, y, xd, yd, reburn=False):
        if self.game.game_stop == 0:
            if reburn:
                self.x = START_X + LEFT_MOVE
                self.y = START_Y
                self.position = [0, 0]
                self.player_img = pygame.transform.scale(self.images[self.direction][self.state], (int(PLAYER_SPEED), int(PLAYER_SPEED)))
                screen.blit(self.player_img, (self.x, self.y))
            else:
                if True:
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
        self.player_img = pygame.transform.scale(self.images[self.direction][self.state], (int(PLAYER_SPEED), int(PLAYER_SPEED)))
        screen.blit(self.player_img, (self.x, self.y))
    
    def render_ui(self, screen):
        img = pygame.transform.scale(pygame.image.load(r'data/sprites/mobs/hpframe.png'), (int(PLAYER_SPEED / 1.5), int(PLAYER_SPEED / 1.5)))
        screen.blit(img, (int(self.x + PLAYER_SPEED // 4), int(self.y + PLAYER_SPEED // 2)))
        pygame.draw.rect(screen, (255, 0, 0), (self.x + PLAYER_SPEED // 2.2, self.y + PLAYER_SPEED // 1.35, self.hp // self.hptick, int(PLAYER_SPEED / 1.5) // 6))

    def hp_add(self, dmg):
        self.hp += dmg
        if self.hp <= 0:
            self.kill()
    
    def kill(self):
        if self in self.game.obj:
            self.state = PLAYER_DEAD
            self.game.obj.remove(self)
            if self.attack_1():
                self.stop = 1
                self.game.player.attacked = 1
            else:
                self.stop = 0
                self.game.player.attacked = 0
            self.game.player.attacked = 0
            self.game.killed_mobs.append(self)
            self.game.play_music(self.musik_deth)
            pygame.mixer.music.stop()

    def contact_check(self, obj):
        if self.game.game_stop == 0:
            res = False
            for el in obj:
                if el.name == 'Ork' and el != self:
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
                    if self.position[0] == el_x and self.position[1]  == el_y:
                        return True
                    else:
                        res = False
            if self.direction == LOOK_RIGHT:
                if self.position[0] == self.player.position[0] and self.position[1] == self.player.position[1]:
                    return True
                else:
                    res = False
            elif self.direction == LOOK_DOWN:
                if self.position[0] == self.player.position[0] and self.position[1] == self.player.position[1]:
                    return True
                else:
                    res = False 
            elif self.direction == LOOK_LEFT:
                if self.position[0] == self.player.position[0] and self.position[1] == self.player.position[1]:
                    return True
                else:
                    res = False
            elif self.direction == LOOK_UP:
                if self.position[0] == self.player.position[0] and self.position[1]  == self.player.position[1]:
                    return True
                else:
                    res = False
            return res

    def random_move(self, screen):
        if self.game.game_stop == 0:
            move = random.randint(0, 3)
            obj = self.game.obj
            x,y,xd,yd = False, False, False, False
            self.attack()
            if self.stop == 0 and self.state != PLAYER_SHOOT:
                if move == 0:
                    self.direction = LOOK_UP
                    self.position[1] -= 1
                    if self.position[1] > 15 or self.position[1] < 0 or self.contact_check(obj):
                        self.position[1] += 1
                    else:
                        yd = True
                        self.move(screen, x, y, xd, yd)
                elif move == 1:
                    self.direction = LOOK_DOWN
                    self.position[1] += 1
                    if self.position[1] > 15 or self.position[1] < 0 or self.contact_check(obj):
                        self.position[1] -= 1
                    else:
                        y = True
                        self.move(screen, x, y, xd, yd)
                elif move == 2:
                    self.direction = LOOK_RIGHT
                    self.position[0] += 1
                    if self.position[0] > 21 or self.position[0] < 0 or self.contact_check(obj):
                        self.position[0] -= 1
                    else:
                        x = True
                        self.move(screen, x, y, xd, yd)
                elif move == 3:
                    self.direction = LOOK_LEFT
                    self.position[0] -= 1
                    if self.position[0] > 21 or self.position[0] < 0 or self.contact_check(obj):
                        self.position[0] += 1
                    else:
                        xd = True
                        self.move(screen, x, y, xd, yd)
        
    def attack(self):
        if self.game.game_stop == 0:
            if self.game.player.state != PLAYER_DEAD:
                pos_ork_x, pos_ork_y, pos_p_x, pos_p_y = self.position[0], self.position[1], self.game.player.position[0], self.game.player.position[1]
                res = False
                if pos_ork_x - 1 == pos_p_x and pos_ork_y == pos_p_y:
                    self.direction = LOOK_LEFT
                    if self.game.player in self.game.shelding:
                        self.game.play_music(SHELD)
                    else:
                        self.game.player.hp -= self.damage
                    res = True
                elif pos_ork_x + 1 == pos_p_x and pos_ork_y == pos_p_y:
                    self.direction = LOOK_RIGHT
                    if self.game.player in self.game.shelding:
                        self.game.play_music(SHELD)
                    else:
                        self.game.player.hp -= self.damage
                    res = True
                elif pos_ork_x  == pos_p_x and pos_ork_y - 1 == pos_p_y:
                    self.direction = LOOK_UP
                    if self.game.player in self.game.shelding:
                        self.game.play_music(SHELD)
                    else:
                        self.game.player.hp -= self.damage
                    res = True
                elif pos_ork_x == pos_p_x and pos_ork_y + 1== pos_p_y:
                    self.direction = LOOK_DOWN
                    if self.game.player in self.game.shelding:
                        self.game.play_music(SHELD)
                    else:
                        self.game.player.hp -= self.damage
                    res = True
                if self.attack_1():
                    self.state = PLAYER_SHOOT
                    self.stop = 1
                    self.game.player.attacked = 1
                    if self.game.player not in self.game.shelding:
                        if self.game.player.hp > 0:
                            self.game.play_music(PLAYER_KICK_MUSIC)
                elif not self.attack_1() and self.stop == 1:
                    self.state = PLAYER_ALIVE
                    self.stop = 0
                    self.game.player.attacked = 0

            else:
                self.state = PLAYER_ALIVE
                self.stop = 0
    
    def attack_1(self):
        pos_ork_x, pos_ork_y, pos_p_x, pos_p_y = self.position[0], self.position[1], self.game.player.position[0], self.game.player.position[1]
        res = False
        if pos_ork_x - 1 == pos_p_x and pos_ork_y == pos_p_y:
            res = True
        elif pos_ork_x + 1 == pos_p_x and pos_ork_y == pos_p_y:
            res = True
        elif pos_ork_x == pos_p_x and pos_ork_y - 1 == pos_p_y:
            res = True
        elif pos_ork_x == pos_p_x and pos_ork_y + 1== pos_p_y:
            res = True
        return res


class Portal():
    def __init__(self, game, x, y, screen):
        self.game = game
        self.x = x-1
        self.y = y-1
        self.open = 0
    
    def render(self, screen):
        if self.open == 1:
            self.image = pygame.image.load(r'data/sprites/portal.png')
            self.image = pygame.transform.scale(self.image, (int(PLAYER_SPEED), int(PLAYER_SPEED)))
            screen.blit(self.image, (self.x * int(PLAYER_SPEED) + LEFT_MOVE, self.y * int(PLAYER_SPEED)))

    def contact_check(self):
        if self.open == 1:
            if self.game.player.position[0] == self.x and self.game.player.position[1] == self.y:
                self.game.play_music(pygame.mixer.Sound(r'data/music/portal_tp.mp3'))
                self.game.new_level()
    
    def opening(self):
        if self.open != 1:
            self.game.play_music(pygame.mixer.Sound(r'data/music/portal_open.mp3'))
            self.open = 1