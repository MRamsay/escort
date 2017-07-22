import math, random, pygame, sys
from asteroid import *
from critters import *
from game import *
from turret import *
from bullet import *
import constants


def main():
    '''	Setting up game variables

	'''
    DIFFICULTY = 0
    game = Game()
    pygame.mixer.pre_init(0, 0, 0, 1024)
    pygame.init()
    pygame.mouse.set_visible(False)
    pygame.display.set_caption(constants.GAME_TITLE)
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode([constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT], (pygame.FULLSCREEN))
    background = pygame.image.load(constants.IMAGE_PATH + constants.BACKGROUND_NAME).convert()
    background_transparent = pygame.image.load(constants.IMAGE_PATH + constants.TRANSPARENT_BACKGROUND_NAME).convert()
    scoreFont = pygame.font.Font(constants.IMAGE_PATH + constants.FONT_NAME, 32)
    scoreFontDouble = pygame.font.Font(constants.IMAGE_PATH + constants.FONT_NAME, 64)
    scoreFontQuad = pygame.font.Font(constants.IMAGE_PATH + constants.FONT_NAME, 128)
    asteroid_sprites = pygame.sprite.Group()
    critter_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    other_sprites = pygame.sprite.Group()
    turret = Turret(constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
    other_sprites.add(turret)

    ticktock = 1
    game_over = False
    wait_time = constants.FPS

    wait_time_minimum = [120, 40, 30]

    livesText = scoreFont.render("Lives: " + str(game.get_lives()), True, constants.WHITE)
    scoreText = scoreFont.render("Score: " + str(game.get_score()), True, constants.WHITE)
    Ships_savedText = scoreFont.render(
        "Ships saved: " + str(game.get_Ships_saved()) + " /" + str(constants.SAVED_SHIPS_REQUIRED[DIFFICULTY]), True,
        constants.WHITE)

    '''
    setup background
    '''
    background_x = (-constants.WINDOW_WIDTH / 48)
    transparency_background = pygame.Surface([constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT], 32)
    transparency_background.blit(background_transparent, (background_x, 0))
    transparency_background_reference = pygame.Surface([constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT], 32)
    selection = {"old": 0, "new": 0}
    selection_options = ["EASY", "MEDIUM", "JAZZY"]
    instructions = ["UP/DOWN ARROWS OR W/S KEYS: CHANGE SELECTION", "SPACE: CONFIRM SELECTION/SHOOT",
                    "LEFT/RIGHT ARROWS OR A/D KEYS: MOVE SPACECRAFT", "ESCAPE: EXIT"]
    first_time = True
    star_rect = ((0, 0), (0, 0))
    surface.blit(transparency_background, (0, 0))
    pygame.display.update()
    while game_over == False:

        # print(clock.get_fps())
        updates = []
        clock.tick(constants.FPS)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    selection["old"] = DIFFICULTY
                    if DIFFICULTY == 0:
                        DIFFICULTY = 2
                    else:
                        DIFFICULTY -= 1
                    selection["new"] = DIFFICULTY
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selection["old"] = DIFFICULTY
                    if DIFFICULTY == 2:
                        DIFFICULTY = 0
                    else:
                        DIFFICULTY += 1
                    selection["new"] = DIFFICULTY
                if event.key == pygame.K_SPACE:
                    game_over = True

        scoreText = scoreFontQuad.render(constants.TITLE, True, constants.WHITE)
        surface.blit(scoreText, [(surface.get_width() / 2) - scoreText.get_size()[0] / 2, 100])
        for n, option in enumerate(selection_options):
            needs_rendering = False
            if n == selection["new"]:
                scoreText = scoreFontDouble.render(option, True, constants.RED)
                needs_rendering = True
            elif n == selection["old"]:
                scoreText = scoreFontDouble.render(option, True, constants.WHITE)
                needs_rendering = True
                y_coordinate = (surface.get_height() / 2 - 200) + (100 * (n - 1))
                x_coordinate = ((surface.get_width() / 2) - scoreText.get_size()[0] / 2)
                updates.append([x_coordinate, y_coordinate, scoreText.get_size()[0], scoreText.get_size()[1]])
                surface.blit(scoreText, (x_coordinate, y_coordinate))
            if needs_rendering:
                y_coordinate = (surface.get_height() / 2 - 200) + (100 * (n - 1))
                x_coordinate = ((surface.get_width() / 2) - scoreText.get_size()[0] / 2)
                surface.blit(scoreText, (x_coordinate, y_coordinate))
                updates.append([x_coordinate, y_coordinate, scoreText.get_size()[0], scoreText.get_size()[1]])

        for n in range(0, len(instructions)):
            scoreText = scoreFont.render(instructions[n], True, constants.WHITE)
            y_coordinate = (surface.get_height() / 2 + 300) + (50 * (n - 1))
            x_coordinate = ((surface.get_width() / 2) - scoreText.get_size()[0] / 2)
            surface.blit(scoreText, (x_coordinate, y_coordinate))

        surface.blit(background, star_rect[0], (star_rect))
        updates.append(
            (draw_circle(surface, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT, random_color(100, 255)), (50, 50)))
        pygame.display.update(updates)
        pygame.display.update(star_rect)
        star_rect = updates[-1]

        if first_time:
            for n, option in enumerate(selection_options):
                scoreText = scoreFontDouble.render(option, True, constants.WHITE)
                y_coordinate = (surface.get_height() / 2 - 200) + (100 * (n - 1))
                x_coordinate = ((surface.get_width() / 2) - scoreText.get_size()[0] / 2)
                surface.blit(scoreText, (x_coordinate, y_coordinate))

            first_time = False
            background.blit(surface, (0, 0))
            pygame.display.update()

    background = pygame.image.load(constants.IMAGE_PATH + constants.BACKGROUND_NAME).convert()
    game_over = False
    intro_outro_script(surface, background_transparent, background_x, scoreFont,
                       "Save " + str(constants.SAVED_SHIPS_REQUIRED[DIFFICULTY]) + " of our ships!")

    # Initialise sound objects

    laser = pygame.mixer.Sound(constants.IMAGE_PATH + constants.SOUND_LASER)

    if DIFFICULTY == 2:

        pygame.mixer.music.load(constants.IMAGE_PATH + constants.SOUND_TWISTED)
        pygame.mixer.music.play(-1)

        explosion = pygame.mixer.Sound(constants.IMAGE_PATH + constants.SOUND_SNAP)

        laser.set_volume(0.5)
        explosion.set_volume(0.6)
    else:
        explosion = pygame.mixer.Sound(constants.IMAGE_PATH + constants.SOUND_EXPLOSION)
        laser.set_volume(0.5)
        explosion.set_volume(0.2)

    ''' Main game loop
	
	'''

    while game_over == False:
        surface.blit(background, (background_x, 0))
        seconds = clock.tick(constants.FPS)  # length between frames
        # print(clock.get_fps())
        for event in pygame.event.get():  # keeps program from seeming unrsponsive to OS
            pass

        if ticktock > wait_time:
            ticktock = 0
            if wait_time >= wait_time_minimum[DIFFICULTY]:
                wait_time -= 10
            if len(critter_sprites) < 10:
                if random.randint(0, 10) > 2:
                    critter_sprites.add(
                        Critter(constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT, critter_sprites, constants.FPS))
                elif len(asteroid_sprites) < 3:
                    critter_sprites.add(
                        Critter(constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT, critter_sprites, constants.FPS))
                    asteroid_sprites.add(Asteroids(constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH))
        else:
            ticktock += .5
        for sprite in bullet_sprites:
            sprite.update_position(constants.SPEED, seconds)

        keys = pygame.key.get_pressed()  # Event handling for keys pressed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            background_x = turret.update_position("left", constants.WINDOW_WIDTH, constants.SPEED, seconds,
                                                  background_x)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            background_x = turret.update_position("right", constants.WINDOW_WIDTH, constants.SPEED, seconds,
                                                  background_x)
        if keys[pygame.K_SPACE]:
            if turret.get_can_shoot():
                bullet = Bullet(turret.get_gun_position())
                bullet_sprites.add(bullet)
                laser.play()
            turret.update_can_shoot(False)
        if (keys[pygame.K_SPACE] == False):
            turret.update_can_shoot(True)
        if keys[pygame.K_ESCAPE]:
            game_over = True

        collisions = pygame.sprite.groupcollide(critter_sprites, bullet_sprites, False,
                                                True)  # check for collisions of bullets and critters
        if collisions:
            for critters in collisions:
                explosion.play()
                critters.shot(game)
                pygame.draw.circle(surface, (255, 150, 0),
                                   [(critters.get_position()[0] + (critters.get_dimensions()[0]) / 2),
                                    (critters.get_position()[1]) + ((critters.get_dimensions()[1]) / 2)], 100)
        collisions = pygame.sprite.groupcollide(asteroid_sprites, bullet_sprites, False, True)
        if collisions:
            for Asteroid in collisions:
                Asteroid.shot(game)
                explosion.play()
        for sprite in critter_sprites:
            sprite.update_position(constants.SPEED, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT, game, seconds,
                                   critter_sprites)  # update critter positions
        for sprite in asteroid_sprites:
            sprite.update_position(constants.SPEED, constants.WINDOW_WIDTH, game, seconds)
        for n in range(0, 3):
            if n == 0 and game.get_updated_variables()[n]:
                livesText = scoreFont.render("Lives: " + str(game.get_lives()), True, constants.WHITE)
            elif n == 1 and game.get_updated_variables()[n]:
                scoreText = scoreFont.render("Score: " + str(game.get_score()), True, constants.WHITE)
            elif n == 2 and game.get_updated_variables()[n]:
                Ships_savedText = scoreFont.render(
                    "Ships saved: " + str(game.get_Ships_saved()) + " /" + str(
                        constants.SAVED_SHIPS_REQUIRED[DIFFICULTY]), True,
                    constants.WHITE)

        if random.randint(0, 2) < 1:
            draw_circle(surface, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT, random_color(100, 250))
        asteroid_sprites.draw(surface)
        bullet_sprites.draw(surface)
        other_sprites.draw(surface)
        critter_sprites.draw(surface)
        surface.blit(livesText, (10, 260))
        surface.blit(scoreText, (10, 230))
        surface.blit(Ships_savedText, (10, 200))
        pygame.display.update()
        surface.fill(constants.BLACK)  #
        if game.get_Ships_saved() >= constants.SAVED_SHIPS_REQUIRED[DIFFICULTY]:
            game_over = True
        if game.get_lives() <= 0:
            game_over = True
        clock.tick(constants.FPS)

    surface.fill(constants.BLACK)  # clear surface
    pygame.mixer.music.fadeout(1600)
    if game.get_Ships_saved() < constants.SAVED_SHIPS_REQUIRED[DIFFICULTY]:
        intro_outro_script(surface, background_transparent, background_x, scoreFont,
                           "Game over. Score: " + str(game.get_score()))
        main()
    else:
        intro_outro_script(surface, background_transparent, background_x, scoreFont,
                           "Winner! Score: " + str(game.get_score()))
        main()


def intro_outro_script(surface, background, background_x, scoreFont, text):
    surface.blit(background, (background_x, 0))
    scoreText = scoreFont.render(text, True, constants.WHITE)  # create new screen with gameover text on it
    surface.blit(scoreText, (
        (surface.get_width() / 2) - scoreText.get_size()[0] / 2, surface.get_height() / 2))  # blit to surface, centered
    pygame.display.update()  # draw to screen
    pygame.time.wait(1500)


def random_color(minimum, maximum):
    r = random.randint(minimum, maximum)
    g = random.randint(minimum, maximum)
    b = random.randint(minimum, maximum)
    colour = [r, g, b]
    return colour


def random_color_greyscale(minimum, maximum):
    r = random.randint(minimum, maximum)
    colour = [r, r, r]
    return colour


def draw_circle(screen, WINDOWWIDTH, WINDOWHEIGHT, color):
    x = random.randint(1, WINDOWWIDTH)
    y = random.randint(1, WINDOWHEIGHT)
    size = random.randint(1, 5)
    pygame.draw.circle(screen, color, (x, y), size)
    return (x - 25, y - 25)


if __name__ == '__main__':
    main()
