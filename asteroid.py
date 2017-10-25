import pygame
import random
import constants
from SpriteObject import SpriteObject

class AsteroidBuilder:

    def __init__(self, game):
        self.game = game

    def build(self):
        return Asteroids(self.game)


class Asteroids(SpriteObject):

    image_reference = pygame.image.load("images/Asteroid.png")

    def __init__(self, game):

        self.rotation_change = random.uniform(-1, 1)
        self.rotation_degrees = 0

        image = Asteroids.image_reference
        rect = image.get_rect()

        y_pos = random.randint(rect.height / 2, (constants.WINDOW_WIDTH - rect.height))

        self.direction = random.choice(["left", "right"])  # which way to go
        if self.direction == "left":
            x_pos = constants.WINDOW_WIDTH + rect.x
            velocity = -constants.SPEED
        else:
            x_pos = (0 - rect.x)
            velocity = constants.SPEED

        position = (x_pos, y_pos)

        SpriteObject.__init__(self, game=game, image=Asteroids.image_reference, velocity_x=velocity, health=5, position=position)

    def update(self):

        super(Asteroids, self).update()

        self.rotation_degrees += self.rotation_change
        self.image = pygame.transform.rotate(self.image_reference, self.rotation_degrees)

        if self.rect.x > (constants.WINDOW_WIDTH + self.rect.x):
            self.succeed()
        elif self.rect.x < (0 - self.rect.x):
            self.succeed()

    def shot(self):
        super(Asteroids, self).shot()

