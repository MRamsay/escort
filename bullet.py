import pygame
import constants


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.x = position["x"] - (self.rect.width / 2)
        self.rect.y = position["y"]

        self.velocity_x = 0
        self.velocity_y = -constants.SPEED * 3

    def update_position(self):
        if self.rect.y >= self.rect.height:
            self.rect.y += self.velocity_y * constants.TICK_PERIOD
        else:
            self.kill()

    def get_position(self):
        return [self.rect.x, self.rect.y]
