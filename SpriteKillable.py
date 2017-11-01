from SpriteObject import SpriteObject


class SpriteKillable(SpriteObject):

    def __init__(self, image, game, velocity_x=0, velocity_y=0, time=0, position=(0, 0),
                 kill_score=0, succeed_score=0, health=1,):

        SpriteObject.__init__(self, image, velocity_x=velocity_x, velocity_y=velocity_y, time=time, position=position)

        self.game = game

        self.kill_score = kill_score

        # if sprite goes off screen, or some other accomplishment
        self.succeed_score = succeed_score
        self.health = health

    def succeed(self):
        self.game.update_score(self.succeed_score)
        self.kill()

    def shot(self):
        self.health -= 1
        if self.health < 1:
            self.game.update_score(self.kill_score)
            self.kill()

