import pygame


LEVEL = 1
pygame.init()
displayInfo = pygame.display.Info()
SCREEN_WIDTH = round(displayInfo.current_w * 0.9)
SCREEN_HEIGHT = round(displayInfo.current_h * 0.9)
BOARD_W = 22
BOARD_H = 16
LOOK_RIGHT = 0
LOOK_DOWN = 1
LOOK_LEFT = 2
LOOK_UP = 3

PLAYER_ALIVE = 0
PLAYER_SHOOT = 1
PLAYER_DEAD = 2

START_X = 0
START_Y = 0

PLAYER_SPEED = int((SCREEN_HEIGHT - 100) // BOARD_H)
LEFT_MOVE = (SCREEN_WIDTH - PLAYER_SPEED * BOARD_W) // 2

POSITION = [0, 0]

MAX_HP = 100
MAX_MP = 100

MAX_HP_P = 100
MAX_MP_P = 100

X, Y, D = 0, 1, 2

PLAYER_KICK_MUSIC = pygame.mixer.Sound(r'data/music/player_kick.mp3')
PLAYER_DEATH_MUSIC = pygame.mixer.Sound(r'data/music/player_death.mp3')

ORK_DEATH_MUSIC = pygame.mixer.Sound(r'data/music/ork_death.mp3')
ORK_KICK_MUSIC = pygame.mixer.Sound(r'data/music/ork_kick.mp3')

DRAGON_DEATH_MUSIC = pygame.mixer.Sound(r'data/music/dragon_death.mp3')
DRAGON_KICK_MUSIC = pygame.mixer.Sound(r'data/music/dragon_kick.mp3')

STONE1_KICK_MUSIC = pygame.mixer.Sound(r'data/music/stone_death.mp3')
STONE1_DEATH_MUSIC = pygame.mixer.Sound(r'data/music/stone_death1.mp3')

BOOM = pygame.mixer.Sound(r'data/music/boom.mp3')
FIREBALL = pygame.mixer.Sound(r'data/music/dragon_attack.mp3')

SHELD = pygame.mixer.Sound(r'data/music/sheld.mp3')

CHEST_OPEN = pygame.mixer.Sound(r'data/music/chest_open.mp3')



FIRE_ARROW_COUNT = 90

SHELD_COUNT = 40
