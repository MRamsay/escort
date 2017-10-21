import pygame


# the position of the object interpolated between game updates
def display_position(delta_t, spr):
    x = spr.rect.x - (spr.velocity_x * delta_t)
    y = spr.rect.y - (spr.velocity_y * delta_t)

    return x, y


class InterpolateDrawGroup(pygame.sprite.Group):

    def __init__(self):
        super(InterpolateDrawGroup, self).__init__()

    def draw(self, surface, delta_t):
        sprites = self.sprites()

        for spr in sprites:
            pos = display_position(delta_t, spr)

            surface.blit(spr.image, pos)

