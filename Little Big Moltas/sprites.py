# Sprite classes
import pygame as pg
from random import uniform
from settings import *
from math import pi, atan2, degrees
vec = pg.math.Vector2

def get_angle(origin, destination):
    """Returns angle in radians from origin to destination.
        This is the angle that you would get if the points were
        on a cartesian grid. Arguments of (0,0), (1, -1)
        return pi/4 (45 deg) rather than  7/4.
        """
    x_dist = destination[0] - origin[0]
    y_dist = destination[1] - origin[1]
    return atan2(-y_dist, x_dist) % (2 * pi)

class Spritesheet(object):
    # class for handling spritesheets
    def __init__(self, filename):
        # initialize spritesheet object
        self.ss =  pg.image.load(filename).convert_alpha()

    def images_at(self, rect_list):
        # loads images in a list at given rect
        image_list = []
        for rect in rect_list:
            image = pg.Surface(rect.size)
            image.set_colorkey(COLOUR_KEY)
            image.blit(self.ss, (0, 0), rect)
            image_list.append(image)
        return image_list

class MOB(pg.sprite.Sprite):
    def __init__(self, game, spritesheet, graphics, x, y, haste=1, box=NORMAL_SIZE):

        # initializing mob sprite
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect((x, y), box)
        self.img = pg.Surface(self.rect.size)
        self.img.fill(YELLOW)

        # initializing dynamics
        self.pos = TILESIZE * vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.haste = haste

        # initializing animation parametres
        self.left = True
        self.attack = False
        self.walking = True
        self.in_air = False
        self.last_update = 0
        self.box = box
        self.angle = 0

        current_frame_leg = 0
        current_frame_torso = 0
        current_frame_hands = 0
        self.current_frame = [current_frame_leg, current_frame_torso, current_frame_hands]

        self.hands_base = pg.Surface(((2*self.box[0], 2*self.box[1]/3)))
        self.hands_base.fill(LIGHTGREY)
        self.hands_base.set_colorkey(LIGHTGREY)
        self.hands_base_left = self.hands_base.copy()
        self.hands_base_left.set_colorkey(LIGHTGREY)

        # initializing animation surfaces
        self.legs = pg.Surface((self.box[0], self.box[1]/2))
        self.torso = pg.Surface((self.box[0], 2*self.box[1]/3))
        self.hands = self.hands_base.copy()

        leg_graphics = Spritesheet(spritesheet).images_at(graphics[0])
        # idle_leg_graphics = Spritesheet(spritesheet).images_at(graphics[0])
        torso_graphics = Spritesheet(spritesheet).images_at(graphics[1])
        hands_graphics = Spritesheet(spritesheet).images_at(graphics[2])
        idle_torso_graphics = Spritesheet(spritesheet).images_at(graphics[3])
        self.graphics = [leg_graphics, torso_graphics, hands_graphics, idle_torso_graphics]

        leg_image = self.graphics[0][0]
        torso_image = self.graphics[1][0]
        hands_image = self.graphics[2][0]
        idle_torso_image = self.graphics[3][0]
        self.images_r = [leg_image, torso_image, hands_image]
        # self.images_l = [pg.transform.flip(image, True, False) for image in self.images_r]
        self.images = self.images_r

        base_rect = self.hands_base.get_rect().center
        base_pos = (base_rect[0] - self.box[0]/4, base_rect[1] - self.box[0]/4)
        self.hands_base.blit(self.images[2], base_pos)
        self.hands_base_left.blit(pg.transform.flip(self.images[2], False, True), base_pos)

        # initializing body rect_list
        self.legs_rect = self.legs.get_rect()
        self.torso_rect = self.torso.get_rect()
        self.hands_rect = self.hands_base.get_rect(center=self.get_pivot())

        self.pivot = self.get_pivot()

    def animate_surface(self, index, left):

        new_frame = (self.current_frame[index] + 1) % len(self.graphics[index])
        self.current_frame.pop(index)
        self.current_frame.insert(index, new_frame)

        new_image = self.graphics[index][self.current_frame[index]]
        if left:
            new_image = pg.transform.flip(new_image, True, False)
        self.images.pop(index)
        self.images.insert(index, new_image)

    def animate_surface1(self, index, graphics, left):

        new_frame = (self.current_frame[index] + 1) % len(graphics)
        self.current_frame.pop(index)
        self.current_frame.insert(index, new_frame)

        new_image = graphics[self.current_frame[index]]
        if left:
            new_image = pg.transform.flip(new_image, True, False)
        self.images.pop(index)
        self.images.insert(index, new_image)


    def animation(self):

        self.legs_rect.midtop = (self.rect.x + self.box[0]/2, self.rect.y + self.box[1]/2)
        self.torso_rect.topleft = (self.rect.x, self.rect.y)
        self.hands_rect.center = (self.rect.x + self.box[0]/4, self.rect.y + self.box[1]/3)

        # rotate hands
        mouse_pos =  pg.mouse.get_pos()
        self.pivot = self.get_pivot()

        # check direction
        angle = get_angle(self.pivot, mouse_pos)
        if pi/2 < angle < 3*pi/2:
            self.left = True
        else:
            self.left = False
        self.rotate_to(mouse_pos, self.left)



        now = pg.time.get_ticks()


        if now - self.last_update > FRAMERATE:

            # hands animation when attacking
            if self.attack:
                self.animate_surface(2, self.left)

            # torso animation when moving
            # self.animate_surface(3, self.left)
            if self.walking:
                self.animate_surface(1, self.left)
            elif self.in_air:
                pass


            # leg animation when moving
            if self.vel.x > 0:
                self.animate_surface(0, False)
            elif self.vel.x < 0:
                self.animate_surface(0, True)

            self.last_update = now

    def get_pivot(self):
        torso_rect = self.game.camera.apply_body(self.torso_rect)
        return torso_rect.x + self.box[0]/2, torso_rect.y + self.box[1]/2

    def rotate_to(self, target, left):
        if left:
            base = self.hands_base_left
        else:
            base = self.hands_base
        angle = get_angle(self.pivot, target)
        self.hands = pg.transform.rotate(base, degrees(angle))
        self.hands_rect = self.hands.get_rect(center=self.pivot)


    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    # def rot_topleft(self, image, rect, angle):
    #     """rotate an image while keeping its center"""
    #     rot_image = pg.transform.rotate(image, angle)
    #     rot_rect = rot_image.get_rect()
    #     return rot_image, rot_rect

    def physics(self):
        # MOB physics
        self.angle -= 0.1

        if self.vel.y == 0:
            self.in_air = False
        else:
            self.in_air = True

        if self.vel.x == 0:
            self.walking = False
        else:
            self.walking = True


        # equations of motion
        if self.vel.length() < 0.01:
            self.vel = vec(0, 0)
        self.acc.x = self.acc.x - FRICTION*self.vel.x
        self.acc.y = self.acc.y + G
        self.vel = self.vel + self.acc

        self.pos = self.pos + self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

class Player(MOB):
    def __init__(self, game, spritesheet, graphics, x, y, haste=1, box=NORMAL_SIZE):
        # initializing playable MOB
        MOB.__init__(self, game, spritesheet, graphics, x, y, haste=1, box=NORMAL_SIZE)

    def get_keys(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc = vec(-PLAYER_SPEED, 0)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc = vec(PLAYER_SPEED, 0)


        if keys[pg.K_SPACE]:
            self.vel.y = JUMP

    def update(self):
        # update MOB
        self.get_keys()
        self.physics()
        self.animation()


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, colour):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# class Player1(pg.sprite.Sprite):
#     def __init__(self, game, x, y):
#
#         self.groups = game.all_sprites
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         self.image = pg.Surface((TILESIZE, 2*TILESIZE))
#         self.image.fill(YELLOW)
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.pos = TILESIZE * vec(x, y)
#         self.vel = vec(0, 0)
#         self.in_air = True
