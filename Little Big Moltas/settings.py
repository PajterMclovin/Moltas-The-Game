import pygame as pg
import os
vec = pg.math.Vector2

TITLE = 'little Moltas'
pg.init()
infoObject = pg.display.Info()
WIDTH = int(infoObject.current_w * 0.7)
HEIGHT = int(infoObject.current_h * 0.7)
FPS = 60

# join paths to local file directory
graphics_dir = os.path.join(os.path.dirname(__file__), 'graphics')
alpha_dir = os.path.join(os.path.dirname(__file__), 'alpha')

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTGREY = (100, 100, 100)
PINK = (255, 0, 180, 20)


# map
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# MOB settings
NORMAL_SIZE = (64, 96)

# graphics
game_folder = os.path.dirname(__file__)
COLOUR_KEY = (255, 0, 180, 20)
FRAMERATE = 150
TEST_SS = 'test_ss.png'
TEST_SS_LOC = ([pg.Rect(NORMAL_SIZE[0]*x, 44, NORMAL_SIZE[0], NORMAL_SIZE[1]/2) for x in xrange(3)],
               [pg.Rect(NORMAL_SIZE[0]*x, 55, NORMAL_SIZE[0], 2*NORMAL_SIZE[1]/3) for x in xrange(1)],
               [pg.Rect(NORMAL_SIZE[0]*x, 77, NORMAL_SIZE[0], NORMAL_SIZE[1]/3) for x in xrange(1)])

ALPHA = os.path.join(alpha_dir, 'alpha.txt')
ALPHA_MAP = pg.image.load(os.path.join(alpha_dir, 'alpha_map.png'))
ALPHA_SS = os.path.join(alpha_dir, 'alpha_ss.png')
ALPHA_SS_LOC = ([pg.Rect(NORMAL_SIZE[0]*x, 0, NORMAL_SIZE[0], NORMAL_SIZE[1]/2)  for x in xrange(1,11)],
                [pg.Rect(64*x, 48, 64, 64) for x in xrange(4)],
                [pg.Rect(0, 172, 64, 32), pg.Rect(0, 204, 64, 32)],
                [pg.Rect(64*x, 112, 64, 63) for x in xrange(4)])


# camera
infoObject = pg.display.Info()
CAM_W = infoObject.current_w
CAM_H = infoObject.current_h

# Player settings
PLAYER_SPEED = 0.04
JUMP = -1
GRAVITY = vec(0, 0.1)
G = 0.1
FRICTION = 0.08
