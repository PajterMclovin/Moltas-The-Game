import pygame as pg
from settings import *

class Map(object):
    def __init__(self, txt, png):
        #initialize Map from textfile and graphics from png-file
        self.data = []
        with open(txt, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
        self.background = png
        self.rect = png.get_rect()
        self.rect.topleft = 0, 0


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, focus):
        return focus.rect.move(self.camera.topleft)

    def apply_body(self, body_rect):
        return body_rect.move(self.camera.topleft)


    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 4)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(WIDTH - self.width, x)  # right
        y = max(HEIGHT - self.height, y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
