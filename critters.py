import pygame
import random
import math

import constants


class CritterBuilder:

    def __init__(self, game):
        self.game = game

    def build(self):
        return Critter(self.game)


class Critter(pygame.sprite.Sprite):

    reference_images = {}
    reference_images_moving = {}

    species = ["Ship", "Strawberry", "Alien", "Squid"]
    for choice in species:
        reference_images[choice] = pygame.image.load("images/" + choice + ".png")
        if choice != "Ship":
            reference_images_moving[choice] = pygame.image.load("images/" + choice + "_moving.png")

    def __init__(self, game):

        self.game = game

        self.velocity_x = 0
        self.velocity_y = 0

        pygame.sprite.Sprite.__init__(self)

        self.attitude_angle = 0

        self.timer_max = constants.FPS / 2
        self.timer = 0

        self.tracking = False
        self.tracking_position = [0, 0]

        self._species = random.choice(Critter.species)

        self.image = Critter.reference_images[self._species]

        self.rect = self.image.get_rect()
        self.rect.y = 0 - self.rect.height
        self.rect.x = (random.randint(self.rect.width / 2, (constants.WINDOW_WIDTH - self.rect.width)))

        self.x = self.rect.x
        self.y = self.rect.y

        self.moving_image = False

        if self._species == "Ship":
            self.image = pygame.transform.rotate(self.image, 180)

    def calculate_motion(self, critter_sprites):

        movement_speed = constants.SPEED * constants.TICK_PERIOD

        if self._species != "Ship":
            self.track_ship(critter_sprites)  # Obtain a target

        self.velocity_y = constants.SPEED

        if self.tracking:
            if -movement_speed < self.rect.x - self.tracking_position[0] < movement_speed:
                self.x = self.tracking_position[0]
                self.velocity_x = 0
            elif self.x < self.tracking_position[0]:
                self.velocity_x = constants.SPEED
            else:
                self.velocity_x = -constants.SPEED
        else:
            self.velocity_x = 0

    def update(self, critter_sprites):

        self.calculate_motion(critter_sprites)

        self.timer += 1

        self.x += self.velocity_x * constants.TICK_PERIOD
        self.y += self.velocity_y * constants.TICK_PERIOD

        self.rect.x = self.x
        self.rect.y = self.y

        if self.timer >= self.timer_max and self._species != "Ship":
            if not self.moving_image:
                self.image = Critter.reference_images_moving[self._species]
                self.moving_image = True
            else:
                self.image = Critter.reference_images[self._species]
                self.moving_image = False
            self.timer = 0

        if self.y > constants.WINDOW_HEIGHT:
            if self._species == "Ship":
                self.game.update_score(50)
                self.game.update_ships_saved()
            else:
                self.game.update_score(-10)
                self.game.update_lives(-1)
            self.kill()

    def shot(self):
        if self._species == "Ship":
            self.game.update_score(-50)
            self.game.update_lives(-1)
        else:
            self.game.update_score(10)
        self.kill()

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
