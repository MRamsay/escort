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

    def update_position(self, direction, seconds, background_x):
        if direction == "left" and self.rect.x > 15:
            self.rect.x -= (constants.SPEED * seconds) * 3
            background_x += (constants.SPEED * seconds) * .15
        elif direction == "right" and self.rect.x < (constants.WINDOW_WIDTH - self.rect.width):
            self.rect.x += (constants.SPEED * seconds) * 3
            background_x -= (constants.SPEED * seconds) * .15
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
