import sys
from asteroid import *
from critters import *
from game import *
from turret import *
from bullet import *
from InterpolateDrawGroup import *
from Spawner import *
import constants

game = Game()
pygame.mixer.pre_init(0, 0, 0, 1024)
pygame.init()
pygame.mouse.set_visible(False)
pygame.display.set_caption(constants.GAME_TITLE)
clock = pygame.time.Clock()
surface = pygame.display.set_mode([constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT], (pygame.FULLSCREEN))

background_transparent = pygame.image.load(constants.IMAGE_PATH + constants.TRANSPARENT_BACKGROUND_NAME).convert()
scoreFont = pygame.font.Font(constants.IMAGE_PATH + constants.FONT_NAME, 32)
scoreFontDouble = pygame.font.Font(constants.IMAGE_PATH + constants.FONT_NAME, 64)
scoreFontQuad = pygame.font.Font(constants.IMAGE_PATH + constants.FONT_NAME, 128)


# raycast collision detection. b is a ray, a is a surface
def collided(sprite_a, sprite_b):

    # position = lambda start, velocity, time: start + (velocity*time)

    a_rect = sprite_a.rect
    b_rect = sprite_b.rect

    velocity_y_a = sprite_a.velocity_y
    velocity_y_b = sprite_b.velocity_y

    velocity_x_a = sprite_a.velocity_x
    velocity_x_b = sprite_b.velocity_x

    # sprite's initial position
    y_a_initial = a_rect.y - velocity_y_a * constants.TICK_PERIOD
    y_b_initial = b_rect.y - velocity_y_b * constants.TICK_PERIOD

    x_a_initial = a_rect.x - velocity_x_a * constants.TICK_PERIOD
    x_b_initial = b_rect.x - velocity_x_b * constants.TICK_PERIOD

    collision_time = ((y_b_initial - y_a_initial) / (velocity_y_a - velocity_y_b))
    # if velocity_x_a != velocity_x_b:
    #     collision_time_x = ((x_b_initial - x_a_initial) / (velocity_x_a - velocity_x_b))
    # else:
    #     collision_time_x = collision_time_y

    y_a_collision = y_a_initial + velocity_y_a * collision_time
    x_a_collision = x_a_initial + velocity_x_a * collision_time

    y_b_collision = y_b_initial + a_rect.height + velocity_y_b * collision_time
    x_b_collision = x_b_initial + velocity_x_b * collision_time

    position_a = (x_a_collision, y_a_collision)
    position_b = (x_b_collision, y_b_collision)

    a_collide_rect = sprite_a.image.get_rect(topleft=position_a)
    b_collide_rect = sprite_b.image.get_rect(bottomleft=position_b)

    pygame.draw.rect(surface, (255, 255, 255), a_collide_rect)
    pygame.draw.rect(surface, (255, 0, 0), b_collide_rect)

    return a_collide_rect.colliderect(b_collide_rect) and 0 <= collision_time <= constants.TICK_PERIOD


def menu():

    difficulty = 0
    background_x = (-constants.WINDOW_WIDTH / 48)

    game_over = False

    '''
    Setup Main Menu
    '''

    transparency_background = pygame.Surface([constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT], 32)
    transparency_background.blit(background_transparent, (background_x, 0))

    selection_options = ("EASY", "MEDIUM", "JAZZY")
    instructions = ("UP/DOWN ARROWS OR W/S KEYS: CHANGE SELECTION", "SPACE: CONFIRM SELECTION/SHOOT",
                    "LEFT/RIGHT ARROWS OR A/D KEYS: MOVE SPACECRAFT", "ESCAPE: EXIT")
    first_time = True
    star_rect = ((0, 0), (0, 0))
    surface.blit(transparency_background, (0, 0))
    pygame.display.update()

    instructions_rendered = map(lambda x: scoreFont.render(x, True, constants.WHITE), instructions)

    difficulty_rendered = {}

    for index, option in enumerate(selection_options):
        difficulty_rendered[index] = {}
        difficulty_rendered[index][False] = scoreFontDouble.render(option, True, constants.WHITE)
        difficulty_rendered[index][True] = scoreFontDouble.render(option, True, constants.RED)

    title = scoreFontQuad.render(constants.TITLE, True, constants.WHITE)

    while not game_over:

        # print(clock.get_fps())
        updates = []
        clock.tick(constants.FPS)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_UP or event.key == pygame.K_w:

                    if difficulty == 0:
                        difficulty = 2
                    else:
                        difficulty -= 1

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:

                    if difficulty == 2:
                        difficulty = 0
                    else:
                        difficulty += 1

                if event.key == pygame.K_SPACE:
                    game_over = True

        surface.blit(title, [(surface.get_width() / 2) - title.get_size()[0] / 2, 100])

        for n, option in enumerate(selection_options):
            selected = n == difficulty
            text = difficulty_rendered[n][selected]

            y_coordinate = (surface.get_height() / 2 - 200) + (100 * (n - 1))
            x_coordinate = ((surface.get_width() / 2) - text.get_size()[0] / 2)
            updates.append([x_coordinate, y_coordinate, text.get_size()[0], text.get_size()[1]])
            surface.blit(text, (x_coordinate, y_coordinate))

        for n, instruction in enumerate(instructions_rendered):
            y_coordinate = (surface.get_height() / 2 + 300) + (50 * (n - 1))
            x_coordinate = ((surface.get_width() / 2) - instruction.get_size()[0] / 2)
            surface.blit(instruction, (x_coordinate, y_coordinate))

        fps_rect = show_fps()
        updates.append(fps_rect)

        surface.blit(transparency_background, star_rect[0], star_rect)

        updates.append(
            (draw_circle(surface, random_color(100, 255)), (50, 50)))
        pygame.display.update(updates)

        pygame.display.update(star_rect)

        surface.blit(transparency_background, fps_rect)

        star_rect = updates[-1]

        if first_time:
            for n, option in enumerate(selection_options):
                score_text = scoreFontDouble.render(option, True, constants.WHITE)
                y_coordinate = (surface.get_height() / 2 - 200) + (100 * (n - 1))
                x_coordinate = ((surface.get_width() / 2) - score_text.get_size()[0] / 2)
                surface.blit(score_text, (x_coordinate, y_coordinate))

            first_time = False
            transparency_background.blit(surface, (0, 0))
            pygame.display.update()

    return difficulty


def main():

    difficulty = menu()

    background = pygame.image.load(constants.IMAGE_PATH + constants.BACKGROUND_NAME).convert()

    game_over = False

    background_x = -constants.WINDOW_WIDTH / 48

    intro_outro_script(surface, background_transparent, background_x, scoreFont,
                       "Save " + str(constants.SAVED_SHIPS_REQUIRED[difficulty]) + " of our ships!")

    # Initialise sound objects

    laser = pygame.mixer.Sound(constants.IMAGE_PATH + constants.SOUND_LASER)

    if difficulty == 2:

        pygame.mixer.music.load(constants.IMAGE_PATH + constants.SOUND_TWISTED)
        pygame.mixer.music.play(-1)

        explosion = pygame.mixer.Sound(constants.IMAGE_PATH + constants.SOUND_SNAP)

        laser.set_volume(0.5)
        explosion.set_volume(0.6)
    else:
        explosion = pygame.mixer.Sound(constants.IMAGE_PATH + constants.SOUND_EXPLOSION)
        laser.set_volume(0.5)
        explosion.set_volume(0.2)

    '''
     Main game loop
    
    '''

    wait_time = constants.FPS

    wait_time_minimum = [120, 40, 15]

    critter_sprites = InterpolateDrawGroup()
    ship_sprites = InterpolateDrawGroup()
    asteroid_sprites = InterpolateDrawGroup()
    bullet_sprites = InterpolateDrawGroup()
    other_sprites = InterpolateDrawGroup()

    collide_sprites = pygame.sprite.Group()
    spawner = Spawner(game, collide_sprites, critter_sprites, ship_sprites, asteroid_sprites)

    sprite_groups = (critter_sprites, ship_sprites, asteroid_sprites, bullet_sprites, other_sprites)

    turret = Turret()
    other_sprites.add(turret)

    elapsed_time = pygame.time.get_ticks()
    update_time = constants.TICK_PERIOD

    ticktock = 1

    while not game_over:

        loops = 0

        while elapsed_time < pygame.time.get_ticks() and loops < constants.MAX_FRAME_SKIP:

            loops += 1
            elapsed_time += update_time

            for event in pygame.event.get():  # keeps program from seeming unrsponsive to OS
                pass

            if ticktock > wait_time:
                ticktock = 0
                if wait_time >= wait_time_minimum[difficulty]:
                    wait_time -= 10
                spawner.spawn()

            else:
                ticktock += .5

            for sprite in bullet_sprites:
                sprite.update_position()

            keys = pygame.key.get_pressed()  # Event handling for keys pressed

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                direction = -1
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                direction = 1
            else:
                direction = 0

            background_x = turret.update_position(direction, background_x)

            if keys[pygame.K_SPACE] and turret.get_can_shoot():

                bullet = Bullet(turret.get_gun_position())
                bullet_sprites.add(bullet)
                laser.play()
                turret.update_can_shoot(False)

            turret.update_can_shoot(not keys[pygame.K_SPACE])

            collisions = pygame.sprite.groupcollide(collide_sprites, bullet_sprites, False, True, collided)  # check for collisions of bullets and critters


            for collide in collisions:
                collide.shot()
                explosion.play()
                pygame.draw.circle(surface, (255, 150, 0),
                                   [collide.rect.x + (collide.rect.width / 2),
                                    collide.rect.y + (collide.rect.height / 2)], 100)

            critter_sprites.update(ship_sprites)
            asteroid_sprites.update()
            ship_sprites.update()

            game_over = keys[pygame.K_ESCAPE]

            if game.get_ships_saved() >= constants.SAVED_SHIPS_REQUIRED[difficulty] or game.get_lives() <= 0:
                game_over = True

        surface.blit(background, (background_x, 0))

        if random.randint(0, 2) < 1:
            draw_circle(surface, random_color(100, 250))

        # interpolated draw
        delta = elapsed_time - pygame.time.get_ticks()
        map(lambda x: x.draw(surface, delta), sprite_groups)

        lives_text = scoreFont.render("Lives: {}".format(game.get_lives()), True, constants.WHITE)
        score_text = scoreFont.render("Score: {}".format(game.get_score()), True, constants.WHITE)
        ships_saved_text = scoreFont.render(
            'Ships saved: {}/{}'.format(game.get_ships_saved(), constants.SAVED_SHIPS_REQUIRED[difficulty]),
            True, constants.WHITE)

        surface.blit(lives_text, (10, 60))
        surface.blit(score_text, (10, 30))
        surface.blit(ships_saved_text, (10, 0))

        show_fps()

        pygame.display.update()

        clock.tick()



    # End Game

    surface.fill(constants.BLACK)  # clear surface
    pygame.mixer.music.fadeout(1600)
    if game.get_ships_saved() < constants.SAVED_SHIPS_REQUIRED[difficulty]:
        intro_outro_script(surface, background_transparent, background_x, scoreFont,
                           "Game over. Score: " + str(game.get_score()))

    else:
        intro_outro_script(surface, background_transparent, background_x, scoreFont,
                           "Winner! Score: " + str(game.get_score()))

    main()


def show_fps():
    fps_text = scoreFont.render(str(int(clock.get_fps())), True, (255, 0, 0))

    rect = fps_text.get_rect(top=(constants.WINDOW_HEIGHT - fps_text.get_height()), left=5)

    surface.blit(fps_text, rect)
    return rect


def intro_outro_script(surface, background, background_x, score_font, text):
    surface.blit(background, (background_x, 0))
    score_text = score_font.render(text, True, constants.WHITE)  # create new screen with gameover text on it
    surface.blit(score_text, (
        (surface.get_width() / 2) - score_text.get_size()[0] / 2,
        surface.get_height() / 2))  # blit to surface, centered
    pygame.display.update()  # draw to screen
    pygame.time.wait(1500)


def random_color(minimum, maximum):
    r = random.randint(minimum, maximum)
    g = random.randint(minimum, maximum)
    b = random.randint(minimum, maximum)
    colour = [r, g, b]
    return colour


def draw_circle(screen, color):
    x = random.randint(1, constants.WINDOW_WIDTH)
    y = random.randint(1, constants.WINDOW_HEIGHT)
    size = random.randint(1, 5)
    pygame.draw.circle(screen, color, (x, y), size)
    return x - 25, y - 25


if __name__ == '__main__':
    main()
