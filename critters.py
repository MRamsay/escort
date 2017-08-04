import pygame
import random
import math


class Critter(pygame.sprite.Sprite):
    def __init__(self, WINDOWWIDTH, WINDOWHEIGHT, critter_sprites, FPS):
        self.attitude_angle = 0
        self.timer_max = FPS / 2
        self.timer = 0
        pygame.sprite.Sprite.__init__(self)
        self.tracking = False
        self.tracking_position = [0, 0]
        self._species = random.choice(["Ship", "Strawberry", "Alien", "Squid"])
        self.image = pygame.image.load("images/" + self._species + ".png")
        self.rect = self.image.get_rect()
        self.rect.y = 0 - self.rect.height
        self.rect.x = (random.randint(self.rect.width / 2, (WINDOWWIDTH - self.rect.width)))
        self.moving_image = False
        if self._species == "Ship":
            self.image = pygame.transform.rotate(self.image, 180)
        else:
            self.image_reference = self.image
            self.image_reference_moving = pygame.image.load("images/" + self._species + "_moving.png")

    def update_position(self, speed, WINDOWWIDTH, WINDOWHEIGHT, game, seconds, critter_sprites):
        movement_speed = speed * seconds
        self.track_ship(WINDOWWIDTH, WINDOWHEIGHT, critter_sprites)  # Obtain a target
        self.rect.y += movement_speed
        self.timer += 1
        if self.timer >= self.timer_max and self._species != "Ship":
            if self.moving_image == False:
                self.image = self.image_reference_moving
                self.moving_image = True
            else:
                self.image = self.image_reference
                self.moving_image = False
            self.timer = 0

        if self.tracking:
            if -(movement_speed) < self.rect.x - self.tracking_position[0] < (movement_speed):
                self.rect.x = self.tracking_position[0]
            elif self.rect.x < self.tracking_position[0]:
                self.rect.x += movement_speed
                movement_speed = movement_speed
            else:
                self.rect.x -= movement_speed

        if self.rect.y > (WINDOWHEIGHT):
            if self._species == "Ship":
                game.update_score(50)
                game.update_Ships_saved()
            else:
                game.update_score(-10)
                game.update_lives(-1)
            self.kill()

    def get_position(self):
        return [self.rect.x, self.rect.y]

    def shot(self, game):
        if self._species == "Ship":
            game.update_score(-50)
            game.update_lives(-1)
        else:
            game.update_score(10)
        self.kill()

    def get_species(self):
        return self._species

    def track_ship(self, WINDOWWIDTH, WINDOWHEIGHT, critter_sprites):
        if self._species == "Ship":
            return
        potential_target = math.hypot(WINDOWWIDTH, WINDOWHEIGHT)
        self.tracking = False
        for Critter in critter_sprites:
            if Critter.get_species() == "Ship":
                delta_x = abs(Critter.get_position()[1] - self.get_position()[1])
                delta_y = abs(Critter.get_position()[1] - self.get_position()[1])
                if potential_target > math.hypot(delta_x, delta_y) and Critter.get_position()[1] > self.get_position()[
                    1]:
                    potential_target = math.hypot(delta_x, delta_y)
                    self.tracking = True
                    self.tracking_position = Critter.get_position()

    def get_dimensions(self):
        return [self.rect.width, self.rect.height]
