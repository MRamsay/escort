import pygame
import constants

# a sprite with a certain velocity, health, etc.
# not to be used in itself, should have a child object


class SpriteObject(pygame.sprite.Sprite):

    def __init__(self, game, image, velocity_x=0, velocity_y=0, kill_score=0, succeed_score=0, health=1, time=0, position=(0,0)):
        pygame.sprite.Sprite.__init__(self)

        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

        self.image = image
        self.game = game

        self.kill_score = kill_score

        # if sprite goes off screen, or some other accomplishment
        self.succeed_score = succeed_score

        # sprite dimensions and position
        self.rect = self.image.get_rect()

        self.health = health

        self.time = time

        self.rect.x, self.rect.y = position

    # game AI for movement, to be overridden
    def calculate_motion(self, *args, **kwargs):
        pass

    # every tick, update sprite position, velocity, etc.
    def update(self, *args, **kwargs):

        self.time += constants.TICK_PERIOD

        self.rect.x += self.velocity_x * constants.TICK_PERIOD
        self.rect.y += self.velocity_y * constants.TICK_PERIOD

    def shot(self):
        self.health -= 1
        if self.health < 1:
            self.game.update_score(self.kill_score)
            self.kill()
