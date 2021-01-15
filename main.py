import pygame
import random
from modules.constants import *
from modules.player import *
from pygame.locals import *
from modules.classes import *
from modules.skill import *
from modules.chests import * 
from modules.levels import *

class Main():
    def __init__(self, screen):
        self.game_stop = 0
        pygame.display.set_caption("RPG-V-0.1.0")
        pygame.display.set_icon(pygame.image.load("data/sprites/icon.ico"))
        self.screen = screen
        self.player = Player(name='Archer', game=self)
        self.running = True
        self.projective = []
        self.cell_size = PLAYER_SPEED
        self.obj = []
        self.killed_obj = []
        self.obj.append(self.player)
        self.shelding = []
        self.sheld_active = []
        self.chests = []
        self.board = [[0] * (BOARD_W) for _ in range(BOARD_H)]
        self.no_enough_mp = None
        self.not_mobs_count = 0
        #self.add_tnt(2, 1)
        self.background = pygame.image.load(r'data/sprites\\background_1.png')
        self.level = 0
        self.volume_music = 1
        self.main_loop()

    def event_loop(self):
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_stop = 0
                    self.running = False
                elif event.type == USEREVENT + 1 and self.game_stop == 0:
                    self.player.state = PLAYER_ALIVE
                    pygame.time.set_timer(USEREVENT + 1, 0)
                elif event.type == USEREVENT + 3 and self.game_stop == 0:
                    if self.player.attacked == 0 and self.player.hp < self.player.max_hp and self.player.state == PLAYER_ALIVE:
                        if self.player.hp + self.player.max_hp // 10 > self.player.max_hp:
                            self.player.hp = self.player.max_hp
                        else:
                            self.player.hp += self.player.max_hp // 10
                    if self.player.mp + self.player.max_mp // 10 > self.player.max_mp:
                        self.player.mp = self.player.max_mp
                    else:
                        self.player.mp += self.player.max_mp // 10
                elif event.type == USEREVENT + 4 and self.game_stop == 0:
                    self.shelding.remove(self.player)
                    for el in self.sheld_active:
                        if el.owner == self.player:
                            self.sheld_active.remove(el)
                    self.play_music(pygame.mixer.Sound('data/music/sheld_active.mp3'))
                    pygame.time.set_timer(USEREVENT + 4, 0)
                elif event.type == USEREVENT + 2 and self.game_stop == 0:
                    for ork in self.obj:
                        if ork.name in ['Ork', 'Dragon']:
                            ork.random_move(self.screen)
                elif event.type == pygame.KEYDOWN:
                    y, x, xd, yd = False, False, False, False
                    if self.game_stop == 0:
                        if self.player.state == PLAYER_ALIVE:
                            if event.key == pygame.K_UP:
                                self.player.direction = LOOK_UP
                                self.player.position[1] -= 1
                                POSITION[1] -= 1
                                if self.player.position[1] > 15 or self.player.position[1] < 0 or self.player.contact_check(self.obj):
                                    self.player.position[1] += 1
                                    POSITION[1] += 1
                                else:
                                    yd = True
                                    self.player.move(self.screen, x, y, xd, yd)
                            elif event.key == pygame.K_DOWN:
                                self.player.direction = LOOK_DOWN
                                self.player.position[1] += 1
                                POSITION[1] += 1
                                if self.player.position[1] > 15 or self.player.position[1] < 0 or self.player.contact_check(self.obj):
                                    self.player.position[1] -= 1
                                    POSITION[1] -= 1
                                else:
                                    y = True
                                    self.player.move(self.screen, x, y, xd, yd)
                            elif event.key == pygame.K_RIGHT:
                                self.player.direction = LOOK_RIGHT
                                self.player.position[0] += 1
                                POSITION[0] += 1
                                if self.player.position[0] > 21 or self.player.position[0] < 0 or self.player.contact_check(self.obj):
                                    self.player.position[0] -= 1
                                    POSITION[0] -= 1
                                else:
                                    x = True
                                    self.player.move(self.screen, x, y, xd, yd)
                            elif event.key == pygame.K_LEFT:
                                self.player.direction = LOOK_LEFT
                                self.player.position[0] -= 1
                                POSITION[0] -= 1
                                if self.player.position[0] > 21 or self.player.position[0] < 0 or self.player.contact_check(self.obj):
                                    self.player.position[0] += 1
                                    POSITION[0] += 1
                                else:
                                    xd = True
                                    self.player.move(self.screen, x, y, xd, yd)
                            elif event.key == pygame.K_d:
                                self.player.direction = LOOK_UP
                                self.player.state = PLAYER_DEAD
                                self.player.hp = 0
                                self.player.mp = 0
                            elif event.key == pygame.K_SPACE and self.player.state != PLAYER_SHOOT:
                                self.player.state = PLAYER_SHOOT
                                pos = POSITION
                                if self.player.direction == LOOK_RIGHT:
                                    self.projective.append(Arrow(screen=self.screen, x=self.player.x + 7, y=self.player.y + self.cell_size // 2, direction=self.player.direction, game=self, position=pos, dmg=self.player.arrow_dmg))
                                elif self.player.direction == LOOK_DOWN:
                                    self.projective.append(Arrow(screen=self.screen, x=self.player.x + self.cell_size // 2 - 4, y=self.player.y + 7, direction=self.player.direction, game=self, position=pos, dmg=self.player.arrow_dmg))
                                elif self.player.direction == LOOK_LEFT:
                                    self.projective.append(Arrow(screen=self.screen, x=self.player.x + 7, y=self.player.y + self.cell_size // 2, direction=self.player.direction, game=self, position=pos, dmg=self.player.arrow_dmg))
                                elif self.player.direction == LOOK_UP:
                                    self.projective.append(Arrow(screen=self.screen, x=self.player.x + self.cell_size // 2 - 4, y=self.player.y - 7, direction=self.player.direction, game=self, position=pos, dmg=self.player.arrow_dmg))
                                pygame.time.set_timer(USEREVENT+1, 200)
                                sound = pygame.mixer.Sound('data/music/arrow.mp3')
                                sound.set_volume(self.volume_music)
                                sound.play()
                                pygame.mixer.music.stop()
                            elif event.key == pygame.K_l and self.player.state != PLAYER_SHOOT:
                                pos = POSITION
                                if self.player.mp >= FIRE_ARROW_COUNT:
                                    self.player.state = PLAYER_SHOOT
                                    if self.player.direction == LOOK_RIGHT:
                                        self.projective.append(Fire_arrow(screen=self.screen, x=self.player.x + 7, y=self.player.y + self.cell_size // 2, direction=self.player.direction, game=self, position=pos, dmg=self.player.fire_arrow_dmg, owner=self.player))
                                    elif self.player.direction == LOOK_DOWN:
                                        self.projective.append(Fire_arrow(screen=self.screen, x=self.player.x + self.cell_size // 2 - 4, y=self.player.y + 7, direction=self.player.direction, game=self, position=pos, dmg=self.player.fire_arrow_dmg, owner=self.player))
                                    elif self.player.direction == LOOK_LEFT:
                                        self.projective.append(Fire_arrow(screen=self.screen, x=self.player.x + 7, y=self.player.y + self.cell_size//2, direction=self.player.direction, game=self, position=pos, dmg=self.player.fire_arrow_dmg, owner=self.player))
                                    elif self.player.direction == LOOK_UP:
                                        self.projective.append(Fire_arrow(screen=self.screen, x=self.player.x + self.cell_size // 2 - 4, y=self.player.y - 7, direction=self.player.direction, game=self, position=pos, dmg=self.player.fire_arrow_dmg, owner=self.player))
                                    self.player.mp -= FIRE_ARROW_COUNT
                                    pygame.time.set_timer(USEREVENT+1, 200)
                                    sound = pygame.mixer.Sound('data/music/fire_arrow.mp3')
                                    sound.set_volume(self.volume_music)
                                    sound.play()
                                    pygame.mixer.music.stop()
                                else:
                                    self.play_music(pygame.mixer.Sound('data/music/error_mp.mp3'))
                            elif event.key == pygame.K_x and self.player.state != PLAYER_SHOOT:
                                if self.player.mp >= SHELD_COUNT and self.player not in self.shelding:
                                    self.sheld_active.append(Sheld(screen=self.screen, game=self, owner=self.player))
                                    self.shelding.append(self.player)
                                    self.player.mp -= SHELD_COUNT
                                    pygame.time.set_timer(USEREVENT+4, 10000)
                                    sound = pygame.mixer.Sound('data/music/sheld_active.mp3')
                                    sound.set_volume(self.volume_music)
                                    sound.play()
                                    pygame.mixer.music.stop()
                                elif self.player.mp < SHELD_COUNT:
                                    self.play_music(pygame.mixer.Sound('data/music/error_mp.mp3'))
                            elif event.key == pygame.K_e:
                                if self.player.direction == LOOK_RIGHT:
                                    for el in self.obj:
                                        if el.name == 'Chest' and el.state == 0:
                                            if el.x - 1 == self.player.position[0] and el.y == self.player.position[1]:
                                                el.state = 1
                                                items = el.items
                                                for item in items:
                                                    if self.player.max_hp + item[3] >= 20:
                                                        self.player.max_hp += item[3]
                                                    if self.player.max_mp + item[4] >= 20:
                                                        self.player.max_mp += item[2]
                                                    self.player.arrow_dmg += item[4]
                                                    self.player.fire_arrow_dmg += item[5] 
                                                    self.play_music(CHEST_OPEN)
                                                    pygame.mixer.music.stop()
                                                    self.game_stop = 1
                                                    self.new_item(item)
                                elif self.player.direction == LOOK_DOWN:
                                    for el in self.obj:
                                        if el.name == 'Chest' and el.state == 0:
                                            if el.x == self.player.position[0] and el.y - 1 == self.player.position[1]:
                                                el.state = 1
                                                items = el.items
                                                for item in items:
                                                    if self.player.max_hp + item[3] >= 20:
                                                        self.player.max_hp += item[3]
                                                    if self.player.max_mp + item[4] >= 20:
                                                        self.player.max_mp += item[2]
                                                    self.player.arrow_dmg += item[4]
                                                    self.player.fire_arrow_dmg += item[5] 
                                                    self.play_music(CHEST_OPEN)
                                                    pygame.mixer.music.stop()
                                                    self.game_stop = 1
                                                    self.new_item(item)

                                elif self.player.direction == LOOK_LEFT:
                                    for el in self.obj:
                                        if el.name == 'Chest' and el.state == 0:
                                            if el.x + 1 == self.player.position[0] and el.y == self.player.position[1]:
                                                el.state = 1
                                                items = el.items
                                                for item in items:
                                                    if self.player.max_hp + item[3] >= 20:
                                                        self.player.max_hp += item[3]
                                                    if self.player.max_mp + item[4] >= 20:
                                                        self.player.max_mp += item[2]
                                                    self.player.arrow_dmg += item[4] 
                                                    self.player.fire_arrow_dmg += item[5]
                                                    self.play_music(CHEST_OPEN)
                                                    pygame.mixer.music.stop()
                                                    self.game_stop = 1
                                                    self.new_item(item)
                                elif self.player.direction == LOOK_UP:
                                    for el in self.obj:
                                        if el.name == 'Chest' and el.state == 0:
                                            if el.x == self.player.position[0] and el.y + 1== self.player.position[1]:
                                                el.state = 1
                                                items = el.items
                                                for item in items:
                                                    if self.player.max_hp + item[3] >= 20:
                                                        self.player.max_hp += item[3]
                                                    if self.player.max_mp + item[4] >= 20:
                                                        self.player.max_mp += item[2]
                                                    self.player.arrow_dmg += item[4]
                                                    self.player.fire_arrow_dmg += item[5] 
                                                    self.play_music(CHEST_OPEN)
                                                    pygame.mixer.music.stop()
                                                    self.game_stop = 1
                                                    self.new_item(item)
                        if event.key == pygame.K_r:
                            self.running = False
                            game = Main(self.screen)
                    if event.key == pygame.K_ESCAPE:
                        if self.game_stop == 0:
                            self.game_stop = 1
                            self.pause()
                        else:
                            self.game_stop = 0

        except Exception as ex:
            print(ex)

    def add_stone_1(self, xs, ys):
        self.obj.append(Stone(screen=self.screen, x=xs, y=ys, game=self))

    def add_tnt(self, xs, ys):
        self.obj.append(Tnt(screen=self.screen, x=xs, y=ys, game=self))

    def add_mob_ork(self, x, y):
        self.obj.append(Mob_ork(x=x, y=y, game=self, name='Ork'))
    
    def add_mob_ork_boss(self, x, y):
        self.obj.append(Mob_ork_boss(x=x, y=y, game=self, name='Ork'))
    
    def add_mob_dragon(self, x, y):
        self.obj.append(Mob_dragon(x=x, y=y, game=self, name='Dragon', screen=self.screen))
    
    def add_chest_1(self, x, y):
        self.obj.append(Chest_1_lvl([x,y]))
    
    def add_chest_2(self, x, y):
        self.obj.append(Chest_2_lvl([x,y]))


    def render(self):
        # Прорисовка кадров
        self.player.render_ui(self.screen)
        font = pygame.font.Font(None, 25)
        mp = self.player.mp
        if mp <= 0:
            mp = 0
        text_mp_player = font.render(f'MP:{mp} / {self.player.max_mp}', 1, (0, 0, 0))


        hp = self.player.hp
        if hp <= 0:
            hp = 0
        text_hp_player = font.render(f'{hp} / {self.player.max_hp}', 1, (255, 255, 255))
        text_hp = font.render(f'HP:', 1, (0, 0, 0))

        mp = self.player.mp
        if mp <= 0:
            mp = 0
        text_mp_player = font.render(f'{mp} / {self.player.max_mp}', 1, (255, 255, 255))
        text_mp = font.render(f'MP:', 1, (0, 0, 0))

        faq_text = [font.render(f'"L" - Fire arrow ({self.player.fire_arrow_dmg} dmg; 90 mp)', 1, (0, 0, 0)), font.render(f'"X" - Sheld (10 sec; 40 mp)', 1, (0, 0, 0)), font.render(f'"SPACE" - Shoot ({self.player.arrow_dmg} dmg)', 1, (0, 0, 0))]
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(self.background, (0, 0))
        for el in self.killed_obj:
            el.render(screen=self.screen)
        self.player.render(self.screen)
        for y in range(16):
            for x in range(22):
                black = (0, 0, 0)
                pygame.draw.rect(self.screen, pygame.Color('white'), (LEFT_MOVE + x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size), 1)
        self.background_inv = pygame.image.load('data/sprites/inter.png')
        self.background_inv = pygame.transform.scale(self.background_inv, (22*PLAYER_SPEED, 5*PLAYER_SPEED))
        self.screen.blit(self.background_inv, (LEFT_MOVE,  PLAYER_SPEED * 16))
        #pygame.draw.rect(self.screen, pygame.Color('white'), (LEFT_MOVE, self.cell_size * BOARD_H, self.cell_size * BOARD_W, SCREEN_HEIGHT))
        #screen.blit(text_mp_player, (LEFT_MOVE + 50,  SCREEN_HEIGHT - 50))
        #screen.blit(text_mp_player, (LEFT_MOVE + 50,  SCREEN_HEIGHT - 50))
        for el in self.projective:
            el.render(screen=self.screen)
        for el in self.chests:
            el.render(screen=self.screen)
        for el in self.sheld_active:
            el.render(screen=self.screen)
        for el in self.obj:
            el.render(screen=self.screen)
            if el.name in ['Ork', 'Dragon']:
                el.render_ui(screen=self.screen)

        # рендер hp_bar
        pygame.draw.rect(self.screen, (0, 0, 0), (LEFT_MOVE + 48, SCREEN_HEIGHT - 102, self.player.stoping_hpframe+2, 23), 2)
        pygame.draw.rect(self.screen, (87, 35, 35), (LEFT_MOVE + 50, SCREEN_HEIGHT - 100, self.player.stoping_hpframe-1, 20))
        if self.player.hp > 0:
            self.player.render_ui(self.screen)
        hp_png = pygame.image.load('data/sprites/health.png')
        hp_png = pygame.transform.scale(hp_png, (PLAYER_SPEED//2, PLAYER_SPEED//2))
        self.screen.blit(hp_png, (LEFT_MOVE + 15,  SCREEN_HEIGHT - 105))
        self.screen.blit(text_hp_player, (LEFT_MOVE + 75,  SCREEN_HEIGHT - 98))

        # рендер mp_bar
        pygame.draw.rect(self.screen, (0, 0, 0), (LEFT_MOVE + 48, SCREEN_HEIGHT - 52, self.player.stoping_mpframe+2, 23), 2)
        pygame.draw.rect(self.screen, (0, 93, 168), (LEFT_MOVE + 50, SCREEN_HEIGHT - 50, self.player.stoping_hpframe-1, 20))
        if self.player.mp > 0:
            self.player.render_mp(self.screen)
        mp_png = pygame.image.load('data/sprites/mana.png')
        mp_png = pygame.transform.scale(mp_png, (PLAYER_SPEED//2, PLAYER_SPEED//2))
        self.screen.blit(mp_png, (LEFT_MOVE + 15,  SCREEN_HEIGHT - 55))
        self.screen.blit(text_mp_player, (LEFT_MOVE + 75,  SCREEN_HEIGHT - 49))

        clock = pygame.time.Clock()
        fps = 60
        clock.tick(fps)
        font = pygame.font.Font(None, 30)
        fps_text = font.render(f'{fps-clock.tick(fps)}', 1, (0, 230, 0))
        self.screen.blit(fps_text, (0,  0))


        # faq
        i = 0
        for el in faq_text:
            self.screen.blit(el, (LEFT_MOVE + 300,  SCREEN_HEIGHT - 45 - i))
            i += 25
        pygame.display.flip()
    
    def return_music(self):
        self.music.play()

    def start_menu(self):
        arr_c = 4
        self.show = True
        font = pygame.font.SysFont('comicsansms', 35)
        font2 = pygame.font.SysFont('comicsansms', 37)
        menu_background = pygame.image.load('data/sprites/main_menu.png')
        arr =  pygame.image.load('data/sprites/choice.png')
        pygame.mixer.init()
        self.music = pygame.mixer.Sound(r'data/music/main_menu2.mp3')
        musix_play = 0
        self.music.play()
        self.music.set_volume(0.5)
        menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        arr = pygame.transform.scale(arr, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
        m_1 = font.render("New game", True, (255, 255, 255))
        m_2 = font.render("Load game", True, (60, 60, 60))
        m_3 = font.render("Settings", True, (0, 128, 0))
        m_4 = font.render("Quit", True, (255, 0, 0))
        m_5 = font.render("Select level", True, (0, 128, 0))

        self.screen.blit(menu_background, (0, 0))
        while self.show:
            self.screen.blit(m_1, (SCREEN_WIDTH // 2.5, SCREEN_HEIGHT//1.65-60*4))
            self.screen.blit(m_2, (SCREEN_WIDTH // 2.5, SCREEN_HEIGHT//1.65-60*3))
            self.screen.blit(m_3, (SCREEN_WIDTH // 2.5, SCREEN_HEIGHT//1.65-60*2))
            self.screen.blit(m_5, (SCREEN_WIDTH // 2.5, SCREEN_HEIGHT//1.65-60*1))
            self.screen.blit(m_4, (SCREEN_WIDTH // 2.5, SCREEN_HEIGHT//1.65))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.show = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.show = Falseё
                    elif event.key == pygame.K_DOWN and arr_c > 0:
                        arr_c -= 1
                    elif event.key == pygame.K_UP and arr_c < 4:
                        arr_c += 1
                    elif event.key == 13:
                        if arr_c == 4:
                            self.music.stop()
                            self.show = False
                        if arr_c == 3:
                            pass
                        if arr_c == 2:
                            self.music.stop()
                            self.settings()
                        if arr_c == 1:
                            self.music.stop()
                            self.choice_level()
                        if arr_c == 0:
                            self.show = False
                            self.running = False
                            self.music.stop()
                if arr_c == 4:
                    m_1 = font.render("New game", True, (255, 255, 255))
                    m_2 = font.render("Load game", True, (60, 60, 60))
                    m_3 = font.render("Settings", True, (0, 128, 0))
                    m_4 = font.render("Quit", True, (255, 0, 0))
                    m_5 = font.render("Select level", True, (0, 128, 0))
                elif arr_c == 3:
                    m_1 = font.render("New game", True, (0, 128, 0))
                    m_2 = font.render("Load game", True, (255, 255, 255))
                    m_3 = font.render("Settings", True, (0, 128, 0))
                    m_4 = font.render("Quit", True, (255, 0, 0))
                    m_5 = font.render("Select level", True, (0, 128, 0))
                elif arr_c == 2:
                    m_1 = font.render("New game", True, (0, 128, 0))
                    m_2 = font.render("Load game", True, (60, 60, 60))
                    m_3 = font.render("Settings", True, (255, 255, 255))
                    m_4 = font.render("Quit", True, (255, 0, 0))
                    m_5 = font.render("Select level", True, (0, 128, 0))
                elif arr_c == 0:
                    m_1 = font.render("New game", True, (0, 128, 0))
                    m_2 = font.render("Load game", True, (60, 60, 60))
                    m_3 = font.render("Settings", True, (0, 128, 0))
                    m_4 = font.render("Quit", True, (255, 255, 255))
                    m_5 = font.render("Select level", True, (0, 128, 0))
                elif arr_c == 1:
                    m_1 = font.render("New game", True, (0, 128, 0))
                    m_2 = font.render("Load game", True, (60, 60, 60))
                    m_3 = font.render("Settings", True, (0, 128, 0))
                    m_4 = font.render("Quit", True, (255, 0, 0))
                    m_5 = font.render("Select level", True, (255, 255, 255))
            
            pygame.display.update()
    
    def choice_level(self):
        i = 0
        level_c = 1
        texts = []
        for lvl in range(LEVELS):
            self.show = True
            font = pygame.font.SysFont('comicsansms', 35)
            font2 = pygame.font.SysFont('comicsansms', 55)
            menu_background = pygame.image.load('data/sprites/main_menu.png')
            
            menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            if i == 0:
                texts.append([font.render(f"LEVEL: {i+1}", True, (255, 255, 255)), i])
            else:
                texts.append([font.render(f"LEVEL: {i+1}", True, (60, 60, 60)), i])
            i += 1
        list(reversed(texts))
        texts_n = []
        for i in range(len(texts)):
            texts_n.append(texts[-1])
            texts.pop(-1)
        texts = texts_n
        while self.show:
            self.screen.blit(menu_background, (0, 0))
            lelvs = font2.render(f"LEVELS:", True, (255, 0, 0))
            self.screen.blit(lelvs, (SCREEN_WIDTH // 2.6, SCREEN_HEIGHT//12))
            for lvl in texts:
                self.screen.blit(lvl[0], (SCREEN_WIDTH // 2.5, SCREEN_HEIGHT//6+60*lvl[1]))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.show = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.show = False
                    elif event.key == pygame.K_DOWN and level_c < LEVELS:
                        level_c += 1
                    elif event.key == pygame.K_UP and level_c > 1:
                        level_c -= 1
                    elif event.key == 13:
                        self.level = level_c -1
                        self.show = False
                recolor = [font.render(f"LEVEL: {level_c}", True, (255, 255, 255)), level_c-1]
                for el in texts:
                    if el[1] == level_c - 1:
                        texts[texts.index(el)] = recolor
                    else:
                        texts[texts.index(el)] = [font.render(f"LEVEL: {el[1]+1}", True, (60, 60, 60)), el[1]]
            pygame.display.update()

    def pause(self):
        arr_c = 5
        self.show = True
        back_ground_pause = pygame.image.load('data/sprites/pause.png')
        back_ground_pause = pygame.transform.scale(back_ground_pause, (SCREEN_WIDTH//6, SCREEN_HEIGHT//3))
        font = pygame.font.SysFont('comicsansms', 35)
        menu_background = pygame.image.load('data/sprites/main_menu.png')
        arr =  pygame.image.load('data/sprites/choice.png')
        
        menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        arr = pygame.transform.scale(arr, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
        m_1 = font.render("Continue", True, (255, 255, 255))
        m_2 = font.render("Main Menu", True, (0, 128, 0))
        m_3 = font.render("Settings", True, (0, 128, 0))
        m_4 = font.render("Quit", True, (255, 0, 0))
        self.music = pygame.mixer.Sound(r'data/music/main_menu2.mp3')
        musix_play = 0
        self.music.play()
        self.music.set_volume(0.5)
        self.screen.blit(menu_background, (0,0))
        self.screen.blit(back_ground_pause, ((SCREEN_WIDTH // 2.5 - 65), (SCREEN_HEIGHT//1.65-60*5-50)))
        while self.show:
            self.screen.blit(m_1, (SCREEN_WIDTH // 2.5, SCREEN_HEIGHT//1.65-60*5))
            self.screen.blit(m_2, (SCREEN_WIDTH // 2.5, SCREEN_HEIGHT//1.65-60*4))
            self.screen.blit(m_3, (SCREEN_WIDTH // 2.5, SCREEN_HEIGHT//1.65-60*3))
            self.screen.blit(m_4, (SCREEN_WIDTH // 2.5, SCREEN_HEIGHT//1.65-60*2))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.show = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.show = False
                    elif event.key == pygame.K_DOWN and arr_c > 1:
                        arr_c -= 1
                    elif event.key == pygame.K_UP and arr_c < 5:
                        arr_c += 1
                    elif event.key == 13:
                        if arr_c == 5:
                            self.show = False
                            self.game_stop = 0
                            self.music.stop()
                        elif arr_c == 4:
                            self.music.stop()
                            self.show = False
                            self.running = False
                            game = Main(self.screen)
                        if arr_c == 3:
                            self.music.stop()
                            self.settings(True)
                        if arr_c == 2:
                            self.show = False
                            self.music.stop()
                            self.running = False
                    elif event.key == pygame.K_ESCAPE:
                            self.show = False
                            self.music.stop()
                            self.game_stop = 0
                if arr_c == 5:
                    m_1 = font.render("Continue", True, (255, 255, 255))
                    m_2 = font.render("Main Menu", True, (0, 128, 0))
                    m_3 = font.render("Settings", True, (0, 128, 0))
                    m_4 = font.render("Quit", True, (255, 0, 0))
                elif arr_c == 4:
                    m_1 = font.render("Continue", True, (0, 128, 0))
                    m_2 = font.render("Main Menu", True, (255, 255, 255))
                    m_3 = font.render("Settings", True, (0, 128, 0))
                    m_4 = font.render("Quit", True, (255, 0, 0))
                elif arr_c == 3:
                    m_1 = font.render("Continue", True, (0, 128, 0))
                    m_2 = font.render("Main Menu", True, (0, 128, 0))
                    m_3 = font.render("Settings", True, (255, 255, 255))
                    m_4 = font.render("Quit", True, (255, 0, 0))
                elif arr_c == 2:
                    m_1 = font.render("Continue", True, (0, 128, 0))
                    m_2 = font.render("Main Menu", True, (0, 128, 0))
                    m_3 = font.render("Settings", True, (0, 128, 0))
                    m_4 = font.render("Quit", True, (255, 255, 255))
            
            pygame.display.update()
            
    def game_over(self):
        img = pygame.image.load('data/sprites/you_dead.jpg')
        img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game_stop = 2
        x = -SCREEN_WIDTH
        while x < 0:
            x += 2
            if self.game_stop == 2:
                self.screen.blit(img, (x, 0))
                pygame.display.flip()
                self.event_loop()
        import time
        time.sleep(0.5)
        self.running = False
        game = Main(self.screen)


    def new_item(self, item):
        arr_c = 1
        font = pygame.font.SysFont('comicsansms', 35)
        item_name = item[0]
        item_type = ['Poison', 'Amulet', 'Wear', 'Item'][item[1]-1]
        item_mp_bonus = item[2]
        item_hp_bonus = item[3]
        item_arr_damage_bonus = item[4]
        item_skill_bonus = item[5]
        text_1 = font.render("New Item:", True, (255, 215, 0))
        text_item_name = font.render(f"{item_name}", True, (255, 255, 255))
        text_item_mp_bonus = font.render(f"{item_mp_bonus}", True, (255, 0, 0))
        text_item_hp_bonus = font.render(f"{item_hp_bonus}", True, (255, 0, 0))
        text_item_arr_damage_bonus = font.render(f"{item_arr_damage_bonus}", True, (255, 0, 0))
        text_item_skill_bonus = font.render(f"{item_skill_bonus}", True, (255, 0, 0))

        text_mp_bonus = font.render(f"Mana Bonus:", True, (177, 179, 177))
        text_hp_bonus = font.render(f"HP Bonus:", True, (177, 179, 177))
        text_arr_damage_bonus = pygame.font.SysFont('comicsansms', 25).render(f"Arrow DMG Bonus:", True, (177, 179, 177))
        text_skill_bonus = pygame.font.SysFont('comicsansms', 20).render(f"Fire Arrow DMG Bonus:", True, (177, 179, 177))
        if item_mp_bonus >= 0:
            text_item_mp_bonus = font.render(f"+{item_mp_bonus}", True, (0, 255, 0))
        if item_hp_bonus >= 0:
            text_item_hp_bonus = font.render(f"+{item_hp_bonus}", True, (0, 255, 0))
        if item_arr_damage_bonus >= 0:
            text_item_arr_damage_bonus = font.render(f"+{item_arr_damage_bonus}", True, (0, 255, 0))
        if item_skill_bonus >= 0:
            text_item_skill_bonus = font.render(f"+{item_skill_bonus}", True, (0, 255, 0))
        
        print(item)
        self.show = True
        back_ground_pause = pygame.image.load('data/sprites/pause.png')
        back_ground_pause = pygame.transform.scale(back_ground_pause, (SCREEN_WIDTH // 3, SCREEN_HEIGHT//2))
        m_1 = font.render("Ok", True, (255, 255, 255))
        self.screen.blit(back_ground_pause, ((SCREEN_WIDTH // 3), (SCREEN_HEIGHT//1.65-60*5-50)))
        while self.show:
            self.screen.blit(m_1, (LEFT_MOVE + PLAYER_SPEED*13.5, PLAYER_SPEED*11.5))
            self.screen.blit(text_1, (LEFT_MOVE + PLAYER_SPEED*9.5, PLAYER_SPEED*5))
            self.screen.blit(text_item_name, (LEFT_MOVE + PLAYER_SPEED*7.5, PLAYER_SPEED*5.9))
            self.screen.blit(text_item_mp_bonus, (LEFT_MOVE + PLAYER_SPEED*11, PLAYER_SPEED*8.5))
            self.screen.blit(text_item_hp_bonus, (LEFT_MOVE + PLAYER_SPEED*11, PLAYER_SPEED*7.5))
            self.screen.blit(text_item_arr_damage_bonus, (LEFT_MOVE + PLAYER_SPEED*11.4, PLAYER_SPEED*9.5))
            self.screen.blit(text_item_skill_bonus, (LEFT_MOVE + PLAYER_SPEED*11.4, PLAYER_SPEED*10.5))
            
            self.screen.blit(text_mp_bonus, (LEFT_MOVE + PLAYER_SPEED*7, PLAYER_SPEED*8.5))
            self.screen.blit(text_hp_bonus, (LEFT_MOVE + PLAYER_SPEED*7, PLAYER_SPEED*7.5))
            self.screen.blit(text_arr_damage_bonus, (LEFT_MOVE + PLAYER_SPEED*7, PLAYER_SPEED*9.7))
            self.screen.blit(text_skill_bonus, (LEFT_MOVE + PLAYER_SPEED*7, PLAYER_SPEED*10.7))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.show = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == 13:
                        if arr_c == 1:
                            self.show = False
                            self.game_stop = 0
                            self.music.stop()
                    elif event.key == pygame.K_ESCAPE:
                            self.show = False
                            self.game_stop = 0
                            self.music.stop()
            
            pygame.display.update()
            


    def settings(self, pause=False):      
        push_button = False, False

        volume = pygame.mixer.music.get_volume()
        self.show = True
        font = pygame.font.SysFont('comicsansms', 35)
        font2 = pygame.font.SysFont('comicsansms', 37)
        menu_background = pygame.image.load('data/sprites/main_menu.png')
        arr =  pygame.image.load('data/sprites/choice.png')
        
        menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        arr = pygame.transform.scale(arr, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
        m_1 = font.render(f"VOLUME: {int(pygame.mixer.music.get_volume()*100)} %", True, (255, 255, 255))

        self.screen.blit(menu_background, (0, 0))
        if pause:
            while self.show:
                self.screen.blit(m_1, (SCREEN_WIDTH // 2.5, SCREEN_HEIGHT//1.65-60*4))
                self.screen.blit(menu_background, (0, 0))
                m_1 = font.render(f"VOLUME: {int(pygame.mixer.music.get_volume()*100)} %", True, (255, 255, 255))
                self.screen.blit(m_1, (SCREEN_WIDTH // 2.5, SCREEN_HEIGHT//1.65-60*4))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.show = False
                        self.running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F1:
                            self.show = False
                        elif event.key == pygame.K_RIGHT and volume < 1:
                            volume += 0.01
                            pygame.mixer.music.set_volume(volume)
                            push_button = True, 1
                        elif event.key == pygame.K_LEFT and volume > 0:
                            volume -= 0.01
                            pygame.mixer.music.set_volume(volume)
                            push_button = True, 0
                        elif event.key == 13:
                            self.show = False
                            self.pause()
                    if event.type==pygame.KEYUP:
                        push_button = False, False
                if push_button != (False, False):
                    if push_button[1] == 1 and volume < 1:
                            volume += 0.01
                            pygame.mixer.music.set_volume(volume)
                    elif push_button[1] == 0 and volume > 0:
                            volume -= 0.01
                            pygame.mixer.music.set_volume(volume)
                    pygame.display.update()
                if volume < 0:
                        volume = 0
                if volume > 1:
                    volume = 1
                self.volume_music = volume
                    
        else:
            while self.show:
                self.screen.blit(m_1, (SCREEN_WIDTH // 2.5, SCREEN_HEIGHT//1.65-60*4))
                self.screen.blit(menu_background, (0, 0))
                m_1 = font.render(f"VOLUME: {int(pygame.mixer.music.get_volume()*100)} %", True, (255, 255, 255))
                self.screen.blit(m_1, (SCREEN_WIDTH // 2.5, SCREEN_HEIGHT//1.65-60*4))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.show = False
                        self.running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F1:
                            self.show = False
                        elif event.key == pygame.K_RIGHT and volume < 1:
                            volume += 0.01
                            push_button = True, 1
                            pygame.mixer.music.set_volume(volume)
                        elif event.key == pygame.K_LEFT and volume > 0:
                            volume -= 0.01
                            push_button = True, 0
                            pygame.mixer.music.set_volume(volume)
                        elif event.key == 13:
                                self.show = False
                                self.start_menu()
                    if event.type==pygame.KEYUP:
                        push_button = False, False
                if push_button != (False, False):
                    if push_button[1] == 1 and volume < 1:
                            volume += 0.01
                            pygame.mixer.music.set_volume(volume)
                    elif push_button[1] == 0 and volume > 0:
                            volume -= 0.01
                            pygame.mixer.music.set_volume(volume)
                    if volume < 0:
                        volume = 0
                    if volume > 1:
                        volume = 1
                    pygame.display.update()
                self.volume_music = volume

    def main_loop(self):
        self.start_menu()
        self.load_level()
        if self.game_stop == 0:
            pygame.time.set_timer(USEREVENT + 2, 1000)
            pygame.time.set_timer(USEREVENT + 3, 1000)
        while self.running == True:
            pygame.mixer.music.set_volume(self.volume_music)
            if self.player.state == PLAYER_DEAD:
                img = pygame.image.load('data/sprites/you_dead.jpg')
                img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.game_stop = 2
                x = -SCREEN_WIDTH
                while x < 0:
                    x += 2
                    if self.game_stop == 2:
                        self.screen.blit(img, (x, 0))
                        pygame.display.flip()
                        self.event_loop()
                import time
                time.sleep(0.5)
                self.running = False
                game = Main(self.screen)
            if self.game_stop == 0:
                for el in self.projective:
                    el.move()
                self.level_check()
                self.render()
            self.event_loop()

    
    def level_check(self):
        if len(self.killed_obj) == self.not_mobs_count:
            self.level += 1
            if self.level <= LEVELS:   
                self.clear_map()         
                self.load_level()
            else:
                self.clear_map()
                self.running = False
                game = Main(self.screen)
                

    def load_level(self):
        levels = [LEVEL1, LEVEL2, LEVEL3, LEVEL4, LEVEL5, LEVEL6, LEVEL7, LEVEL]
        if len(levels) > self.level:
            for y in range(BOARD_H):
                for x in range(BOARD_W):
                    if levels[self.level][y][x] == 1:
                        self.add_stone_1(x + 1, y + 1)
                    elif levels[self.level][y][x] == 2:
                        self.add_mob_ork(x + 1, y + 1)
                        self.not_mobs_count += 1
                    elif levels[self.level][y][x] == -1:
                        self.add_chest_1(x, y)
                    elif levels[self.level][y][x] == -2:
                        self.add_chest_2(x, y)
                    elif levels[self.level][y][x] == 3:
                        self.add_mob_ork_boss(x + 1, y + 1)
                        self.not_mobs_count += 1
                    elif levels[self.level][y][x] == 4:
                        self.add_mob_dragon(x + 1, y + 1)
                        self.not_mobs_count += 1

    def clear_map(self):
        self.obj = []
        self.obj.append(self.player)
        self.killed_obj = []
        self.projective = []
        self.shelding = []
        self.sheld_active = []
        self.not_mobs_count = 0
        self.player.hp = self.player.max_hp
        self.player.mp = self.player.max_mp
        self.player.attacked = 0
        self.player.direction = LOOK_RIGHT
        self.player.state = PLAYER_ALIVE
        self.player.x = START_X + LEFT_MOVE
        self.player.y = START_Y
        self.player.position = [0,0]

    def play_music(self, music):
        sound = music
        sound.set_volume(self.volume_music)
        sound.play()
        pygame.mixer.music.stop()

pygame.init()
size = SCREEN_WIDTH, SCREEN_HEIGHT
screen = pygame.display.set_mode(size)
game = Main(screen)