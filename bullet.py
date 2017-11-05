import pygame
import constants
from SpriteObject import SpriteObject


class Bullet(SpriteObject):

    image = pygame.image.load("images/bullet.png")

    def __init__(self, position):

        width = Bullet.image.get_rect().width

        x = position["x"] - (width / 2)
        y = position["y"]

        position = (x, y)

        velocity_y = -constants.SPEED * 10

        SpriteObject.__init__(self, image=Bullet.image, velocity_y= velocity_y, position=position)

    def update_position(self):
        if self.rect.y >= self.rect.height:
            self.rect.y += self.velocity_y * constants.TICK_PERIOD
        else:
            self.kill()

    def get_position(self):
        return [self.rect.x, self.rect.y]
