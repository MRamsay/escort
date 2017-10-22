import pygame
import constants


class Turret(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(constants.IMAGE_PATH + "Ship.png")
        self.rect = self.image.get_rect()
        self.rect.x = (constants.WINDOW_WIDTH - self.rect.width) / 2
        self.rect.y = constants.WINDOW_HEIGHT - self.rect.height * 1.5
        self.can_shoot = True

        self.velocity_x = 0
        self.velocity_y = 0

    def update_position(self, direction, background_x):

        if direction == -1 and self.rect.left > 0:
            self.velocity_x = -constants.SPEED * 1.5
        elif direction == 1 and self.rect.x < (constants.WINDOW_WIDTH - self.rect.width):
            self.velocity_x = constants.SPEED * 1.5
        else:
            self.velocity_x = 0

        background_x += -self.velocity_x * constants.TICK_PERIOD * 0.02

        self.rect.x += self.velocity_x * constants.TICK_PERIOD

        return background_x

    def get_gun_position(self):
        position = {
            "x": self.rect.x + (self.rect.width / 2),
            "y": self.rect.y - (self.rect.height / 2)
        }
        return position

    def update_can_shoot(self, can_shoot_update):
        self.can_shoot = can_shoot_update

    def get_can_shoot(self):
        return self.can_shoot
