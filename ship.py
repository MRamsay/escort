import random

import constants
import pygame

from SpriteKillable import SpriteKillable


class Ship(SpriteKillable):

    image = pygame.image.load(constants.IMAGE_PATH + "Ship.png")
    image = pygame.transform.rotate(image, 180)

    def __init__(self, game):

        image = Ship.image

        rect = image.get_rect()

        x_pos = random.randint(rect.width / 2, (constants.WINDOW_WIDTH - rect.width))
        y_pos = 0 - rect.height

        position = x_pos, y_pos

        kill_score = -50
        succeed_score = 50

        SpriteKillable.__init__(self, game=game, image=image, velocity_y=constants.SPEED,
                                kill_score=kill_score, succeed_score=succeed_score,
                                position=position)

    def shot(self):

        self.game.update_lives(-1)
        super(Ship, self).shot()

    def update(self):
        super(Ship, self).update()

        if self.rect.y > constants.WINDOW_HEIGHT:
            self.game.update_ships_saved()
            self.succeed()

