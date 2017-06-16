# Project setup
import pygame as pg
import random, os
from settings import *
from sprites import *
from tilemap import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.varFlag = 0 #pg.FULLSCREEN
        # pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), self.varFlag, 32)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.current_level = 0
        self.running = True

    def new_level(self, level):
        # initialize all variables and do all the setup for a new level

        self.map = Map(ALPHA, ALPHA_MAP)

        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()

        self.camera = Camera(self.map.width, self.map.height)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'W':
                    Wall(self, col, row, WHITE)
                if tile == 'B':
                    Wall(self, col, row, RED)
                if tile == 'P':
                    self.player = Player(self, ALPHA_SS, ALPHA_SS_LOC, col, row)

    def new(self, level=0):
        # start a new game
        # set scores etc. to zero
        self.time = 0
        self.new_level(level)

        # run game
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)
            self.update()
            self.events()
            self.draw()
        self.gameover()

    def update(self):
        # Game Loop - update
        self.all_sprites.update()
        self.camera.update(self.player)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():

            # check for closing window
            if (event.type == pg.QUIT
                or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                if self.playing:
                    self.playing = False
                self.running = False

            # switch between window and fullscreen
            if event.type == pg.KEYDOWN and event.key == pg.K_f:
                if self.varFlag == 0:
                    self.varFlag = pg.FULLSCREEN
                    pg.mouse.set_visible(False)
                elif self.varFlag == pg.FULLSCREEN:
                    self.varFlag = 0
                    pg.mouse.set_visible(True)
                self.screen = pg.display.set_mode((WIDTH, HEIGHT), self.varFlag, 32)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        # Game Loop - draw
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))

        # self.screen.blit(self.map.background, self.camera.apply_body(self.map.rect))
        self.screen.fill(PINK)
        # self.draw_grid()
        for wall in self.walls:
            self.screen.blit(wall.image, self.camera.apply(wall))
        for mob in self.mobs:
            self.screen.blit(mob.img, self.camera.apply_body(mob.rect))
            self.screen.blit(mob.images[0], self.camera.apply_body(mob.legs_rect))
            self.screen.blit(mob.images[1], self.camera.apply_body(mob.torso_rect))
            self.screen.blit(mob.hands, mob.hands_rect)


            mouse_pos = vec(pg.mouse.get_pos())
            crosshair = pg.Rect(mouse_pos, (10, 10))
            # player_pos = self.camera.apply_body(mob.rect.left + 32, mob.rect.top + 64)
            pg.draw.rect(self.screen, GREEN, crosshair, 5)


        pg.display.flip()

    def gameover(self):
        print 'game over'
        # self.running = False

    def show_start_screen(self):
        # game splash/start screen
        pass

    def menu(self):
        # game menu
        pass

    def show_gameover_screen(self):
        # game over/continue
        pass

class Text(pg.sprite.Sprite):
    def __init__(self, text, font_input, size, colour, x, y):
        # initialize text sprite
        pg.sprite.Sprite.__init__(self)
        font = pg.font.Font(pg.font.match_font(font_input), size)
        self.surface = font.render(text, True, colour)
        self.rect = self.surface.get_rect()
        self.rect.midtop = (x, y)

    def draw(self, surface):
        # draw text sprite
        surface.blit(self.surface, self.rect)

g = Game()
g.show_start_screen()
g.menu()
while g.running:
    g.new(g.current_level)
    g.show_gameover_screen()

pg.quit()
