import pygame
import random
import math
from SpriteKillable import SpriteKillable

import constants


class CritterBuilder:

    def __init__(self, game):
        self.game = game

    def build(self):
        return Critter(self.game)


class Critter(SpriteKillable):

    reference_images = {}
    reference_images_moving = {}

    species = ["Strawberry", "Alien", "Squid"]
    for choice in species:
        reference_images[choice] = pygame.image.load("images/" + choice + ".png")

        reference_images_moving[choice] = pygame.image.load("images/" + choice + "_moving.png")

    def __init__(self, game):

        self._species = random.choice(Critter.species)

        image = Critter.reference_images[self._species]

        rect = image.get_rect()

        x_pos = random.randint(rect.width / 2, (constants.WINDOW_WIDTH - rect.width))
        y_pos = 0 - rect.height

        kill_score = 10
        succeed_score = -50

        SpriteKillable.__init__(self, game=game, image=image, velocity_y=constants.SPEED,
                                kill_score=kill_score, succeed_score=succeed_score,
                                position=(x_pos, y_pos))

        self.tracking = False
        self.tracking_position = [0, 0]

        self.moving_image = False

        self.timer = 0
        self.timer_max = constants.FPS /2

    def calculate_motion(self, critter_sprites):

        movement_speed = constants.SPEED * constants.TICK_PERIOD

        self.track_ship(critter_sprites)  # Obtain a target

        if self.tracking:
            if -movement_speed < self.rect.x - self.tracking_position[0] < movement_speed:
                self.rect.x = self.tracking_position[0]
                self.velocity_x = 0
            elif self.rect.x < self.tracking_position[0]:
                self.velocity_x = constants.SPEED
            else:
                self.velocity_x = -constants.SPEED
        else:
            self.velocity_x = 0

    def update(self, critter_sprites):

        self.calculate_motion(critter_sprites)

        super(Critter, self).update()

        self.timer += 1

        if self.timer >= self.timer_max:
            if not self.moving_image:
                self.image = Critter.reference_images_moving[self._species]
                self.moving_image = True
            else:
                self.image = Critter.reference_images[self._species]
                self.moving_image = False
            self.timer = 0

        if self.rect.y > constants.WINDOW_HEIGHT:
            self.game.update_lives(-1)
            self.succeed()

    def get_species(self):
        return self._species

    def get_velocity(self):
        return self.velocity_x, self.velocity_y

    # distance from critter to target
    def calculate_distance(self, target):
        delta_x = target.rect.x - self.rect.x
        delta_y = target.rect.y - self.rect.y

        return abs(math.hypot(delta_x, delta_y))

    def get_position(self):
        return [self.rect.x, self.rect.y]

    def track_ship(self, critter_sprites):

        self.tracking = False
        # ships below critter
        targets = [target for target in critter_sprites if
                   target.get_species() == "Ship" and target.get_position()[1] > self.get_position()[1]]

        if targets:
            target = min(targets, key=self.calculate_distance)
            self.tracking_position = target.get_position()
            self.tracking = True

    def get_dimensions(self):
        return [self.rect.width, self.rect.height]
