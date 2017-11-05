import random

import critters
import ship
import asteroid


def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w


# spawn a critter/ship/asteroid
class Spawner():

    def __init__(self, game, collide_group, critter_group, ship_group, asteroid_group):

        self.collide_group = collide_group

        self.critter_group = critter_group
        self.ship_group = ship_group
        self.asteroid_group = asteroid_group

        self.game = game

    def spawn(self):

        # which object, what group it belongs to, its weight
        choices = (
            ((critters.Critter, self.critter_group), 70),
            ((ship.Ship, self.ship_group), 20),
            ((asteroid.Asteroids, self.asteroid_group), 500)
        )

        # choose which kind of creature to spawn
        choice, group = weighted_choice(choices)

        # spawn object
        choice = choice(self.game)
        choice.add(group, self.collide_group)
