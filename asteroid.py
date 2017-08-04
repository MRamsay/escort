import pygame
import random


class AsteroidBuilder:

    def __init__(self, window_height, window_width, speed):
        self.window_height = window_height
        self.window_width = window_width
        self.speed = speed

    def build(self):
        return Asteroids(self.window_height, self.window_width, self.speed)


class Asteroids(pygame.sprite.Sprite):

    image_reference = pygame.image.load("images/Asteroid.png")

    def __init__(self, window_height, window_width, speed):

        pygame.sprite.Sprite.__init__(self)

        self.window_height = window_height
        self.window_width = window_width

        self.rotation_change = random.uniform(-1, 1)
        self.rotation_degrees = 0

        self.image = Asteroids.image_reference
        self.image_reference = self.image

        self.rect = self.image.get_rect()

        self.rect.y = random.randint(self.rect.height / 2, (self.window_width - self.rect.height))

        self.direction = random.choice(["left", "right"])  # which way to go
        if self.direction == "left":
            self.rect.x = self.window_width + self.rect.x
            self.speed = -speed
        else:
            self.rect.x = (0 - self.rect.x)
            self.speed = speed

        self.hit_points = 5  # number of hits it takes

    def update(self, seconds):

        self.rect.x += (self.speed * seconds)

        self.image = pygame.transform.rotate(self.image_reference, self.rotation_degrees)

        self.rect = self.image.get_rect(center=self.rect.center)

        self.rotation_degrees += self.rotation_change

        if self.rect.x > (self.window_width + self.rect.x):
            self.kill()
        elif self.rect.x < (0 - self.rect.x):
            self.kill()

    def shot(self, game):
        if self.hit_points <= 0:
            self.kill()
        else:
            self.hit_points -= 1
