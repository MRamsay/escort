import pygame
import random
import math


class CritterBuilder:

    def __init__(self, window_width, window_height, fps, game, speed):
        self.window_width = window_width
        self.window_height = window_height
        self.fps = fps
        self.game = game
        self.speed = speed

    def build(self):
        return Critter(self.window_width, self.window_height, self.fps, self.game, self.speed)


class Critter(pygame.sprite.Sprite):

    reference_images = {}
    reference_images_moving = {}

    species = ["Ship", "Strawberry", "Alien", "Squid"]
    for choice in species:
        reference_images[choice] = pygame.image.load("images/" + choice + ".png")
        if choice != "Ship":
            reference_images_moving[choice] = pygame.image.load("images/" + choice + "_moving.png")

    def __init__(self, window_width, window_height, fps, game, speed):

        self.window_width = window_width
        self.window_height = window_height
        self.fps = fps
        self.game = game
        self.speed = speed

        pygame.sprite.Sprite.__init__(self)

        self.attitude_angle = 0

        self.timer_max = fps / 2
        self.timer = 0

        self.tracking = False
        self.tracking_position = [0, 0]

        self._species = random.choice(Critter.species)

        self.image = Critter.reference_images[self._species]

        self.rect = self.image.get_rect()
        self.rect.y = 0 - self.rect.height
        self.rect.x = (random.randint(self.rect.width / 2, (self.window_width - self.rect.width)))

        self.moving_image = False

        if self._species == "Ship":
            self.image = pygame.transform.rotate(self.image, 180)

    def update(self, seconds, critter_sprites):

        movement_speed = self.speed * seconds

        if self._species != "Ship":
            self.track_ship(critter_sprites)  # Obtain a target

        self.rect.y += movement_speed
        self.timer += 1

        if self.timer >= self.timer_max and self._species != "Ship":
            if not self.moving_image:
                self.image = Critter.reference_images_moving[self._species]
                self.moving_image = True
            else:
                self.image = Critter.reference_images[self._species]
                self.moving_image = False
            self.timer = 0

        if self.tracking:
            if -movement_speed < self.rect.x - self.tracking_position[0] < movement_speed:
                self.rect.x = self.tracking_position[0]
            elif self.rect.x < self.tracking_position[0]:
                self.rect.x += movement_speed
            else:
                self.rect.x -= movement_speed

        if self.rect.y > self.window_height:
            if self._species == "Ship":
                self.game.update_score(50)
                self.game.update_ships_saved()
            else:
                self.game.update_score(-10)
                self.game.update_lives(-1)
            self.kill()

    def get_position(self):
        return [self.rect.x, self.rect.y]

    def shot(self):
        if self._species == "Ship":
            self.game.update_score(-50)
            self.game.update_lives(-1)
        else:
            self.game.update_score(10)
        self.kill()

    def get_species(self):
        return self._species

    # distance from critter to target
    def calculate_distance(self, target):
        delta_x = target.rect.x - self.rect.x
        delta_y = target.rect.y - self.rect.y

        return abs(math.hypot(delta_x, delta_y))

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
