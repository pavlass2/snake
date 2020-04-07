#!/usr/bin/python

import pyglet
import os
import random
import logger
import keyCash


# global control variables and their initialization
# controls game speed by frame rate, default is 10
game_speed = 10
# width of whole window
window_width = 1080
# height of whole window
window_height = 480
# width of area where score, time and more are showed
score_area_width = 100

# global variables and their initialization
# maximum width where snake can move counted in pixels - that is width minus right side wall
play_field_width = window_width - score_area_width
# maximum height where snake can move counted in pixels - that is height minus top side wall
play_field__height = window_height - 20
# sum of all possible positions snake's head can use
fields = play_field__height * play_field_width / 20
# game stops if this is true
game_over = False
# game already runs if this is true
game_running = False
window = pyglet.window.Window(window_width, window_height)
logger = logger.Logger()
# takes care of user input and its usage
key_cash = keyCash.KeyCash()

# images
snake_img = pyglet.image.load(os.path.join('img', 'snake.png'))
apple_img = pyglet.image.load(os.path.join('img', 'apple.png'))
wall_img = pyglet.image.load(os.path.join('img', 'wall.png'))


# after window is opened, this is done
# and then every time the snake moves
@window.event
def on_draw():
    global game_over
    global snake_body
    window.clear()
    batch = pyglet.graphics.Batch()
    sprites = []
    if game_over:

        label = pyglet.text.Label('Your snake died!',
                                  font_name='Times New Roman',
                                  font_size=36,
                                  x=window.width / 2, y=window.height / 2,
                                  anchor_x='center', anchor_y='center')

        label.draw()

    # else:
    # snake sprites
    for num, snake_part in enumerate(snake_body):
        sprite = pyglet.sprite.Sprite(snake_img, batch=batch)
        sprite.x = snake_part[0]
        sprite.y = snake_part[1]
        sprites.append(sprite)

        # fill empty space in snakes body
        if num + 1 < len(snake_body):
            sprite_filling = pyglet.sprite.Sprite(snake_img, batch=batch)
            if snake_part[0] < snake_body[num + 1][0]:
                # next snake part is on the right side of this part
                sprite_filling.x = snake_part[0] + 10
                sprite_filling.y = snake_part[1]
            elif snake_part[0] > snake_body[num + 1][0]:
                # next snake part is on the left side of this part
                sprite_filling.x = snake_part[0] - 10
                sprite_filling.y = snake_part[1]
            elif snake_part[1] > snake_body[num + 1][1]:
                # next snake part is on the left side of this part
                sprite_filling.y = snake_part[1] - 10
                sprite_filling.x = snake_part[0]
            elif snake_part[1] < snake_body[num + 1][1]:
                # next snake part is on the left side of this part
                sprite_filling.y = snake_part[1] + 10
                sprite_filling.x = snake_part[0]
            sprites.append(sprite_filling)

    # wall sprites
    # horizontal
    counter = 0
    while counter <= play_field_width:
        sprite = pyglet.sprite.Sprite(wall_img, batch=batch)
        sprite.x = counter
        sprite.y = window_height - 20
        sprites.append(sprite)

        sprite = pyglet.sprite.Sprite(wall_img, batch=batch)
        sprite.x = counter
        sprite.y = 0
        sprites.append(sprite)

        counter = counter + 20
    # vertical
    global score_area_width
    counter = 0
    while counter < play_field__height:
        sprite = pyglet.sprite.Sprite(wall_img, batch=batch)
        sprite.x = play_field_width
        sprite.y = counter
        sprites.append(sprite)

        sprite = pyglet.sprite.Sprite(wall_img, batch=batch)
        sprite.x = 0
        sprite.y = counter
        sprites.append(sprite)
        counter = counter + 20

    # apple sprite
    apple_sprite = pyglet.sprite.Sprite(apple_img, batch=batch)
    new_apple_coordinates = apple
    apple_sprite.x = new_apple_coordinates[0]
    apple_sprite.y = new_apple_coordinates[1]
    sprites.append(apple_sprite)

    batch.draw()


# every time user presses key do this
@window.event
def on_key_press(symbol, modifiers):

    # exit app on "Escape" key press
    if symbol == pyglet.window.key.ESCAPE:
        pyglet.app.EventLoop().exit()

    # if user pressed arrow key, save it as last command
    # ignore other inputs
    if symbol == pyglet.window.key.LEFT\
            or symbol == pyglet.window.key.RIGHT\
            or symbol == pyglet.window.key.UP\
            or symbol == pyglet.window.key.DOWN:
        key_cash.add_command(symbol)
    global game_running
    # if game is NOT running yet, start it
    if not game_running:
        game_running = True
        pyglet.clock.schedule_interval(movement, 1 / game_speed)


# calculate the movement
def movement(dt):
    global game_over
    if game_over:
        return
    global snake_body
    # after movement is done, this is were a new part would go
    apple_increment_part = [snake_body[-1][0], snake_body[-1][1]]

    # move every part of the body to the next position
    counter = len(snake_body) - 1
    while counter > 0:
        snake_body[counter][0] = snake_body[counter - 1][0]
        snake_body[counter][1] = snake_body[counter - 1][1]
        counter = counter - 1

    # move head to the new position
    last_command = key_cash.get_last_command()
    if last_command == pyglet.window.key.LEFT:
        if is_alive(snake_body[0][0] - 20, snake_body[0][1]):
            snake_body[0][0] = snake_body[0][0] - 20
            logger.log_debug("Move left")
        else:
            die()
            return
    elif last_command == pyglet.window.key.RIGHT:
        if is_alive(snake_body[0][0] + 20, snake_body[0][1]):
            snake_body[0][0] = snake_body[0][0] + 20
            logger.log_debug("Move right")
        else:
            die()
            return
    elif last_command == pyglet.window.key.UP:
        if is_alive(snake_body[0][0], snake_body[0][1] + 20):
            snake_body[0][1] = snake_body[0][1] + 20
            logger.log_debug("Move up")
        else:
            die()
            return
    elif last_command == pyglet.window.key.DOWN:
        if is_alive(snake_body[0][0], snake_body[0][1] - 20):
            snake_body[0][1] = snake_body[0][1] - 20
            logger.log_debug("Move down")
        else:
            die()
            return

    logger.log_debug("Head position: [" + str(snake_body[0][0]) + ", " + str(snake_body[0][1]) + "]")

    # apple eating
    global apple
    if snake_body[0][0] == apple[0] + 2 and snake_body[0][1] == apple[1] + 2:
        snake_body.append(apple_increment_part)
        apple = generate_random_apple()


def is_alive(x, y):
    # death conditions
    # is snakes's head out of bounds of screen?
    if (x > play_field_width - 18) \
            or (x < 20) \
            or (y > play_field__height - 18) \
            or (y < 20):
        return False

    # check if snake crashed into his body
    counter = 1
    while counter < len(snake_body):
        if snake_body[counter][0] == x and snake_body[counter][1] == y:
            return False
        counter = counter + 1

    # if we got this far, snake is alive
    return True


def die():
    global game_over
    pyglet.clock.unschedule(movement)
    game_over = True
    logger.log_debug("Hit")


# returns array of random 2D coordinates [x, y] in play field thar are not occupied by snake
def generate_random_apple():
    global fields
    global snake_body
    new_apple = None
    # first half of the game
    if len(snake_body) < fields / 0.05:
        while not new_apple:
            suggested_coordinates = [random.randrange(20, play_field_width, 20), random.randrange(20, play_field__height, 20)]
            snake_body_contains_suggested_coordinates = False
            for snake_part in snake_body:
                if suggested_coordinates[0] == snake_part[0] - 2 and suggested_coordinates[1] == snake_part[1] - 2:
                    snake_body_contains_suggested_coordinates = True
                    break

            if not snake_body_contains_suggested_coordinates:
                new_apple = suggested_coordinates
    # snake occupies most of game fields so we need to now what fields are currently empty
    else:
        global non_occupied_fields
        if not non_occupied_fields:
            # this is first time this mode is used, we need to create array of non occupied field
            y = 0
            while y <= play_field__height:
                x = 0
                while x <= play_field_width:
                    for sneak_part in snake_body:
                        occupied = False
                        if sneak_part[0] - 2 == x and sneak_part[1] - 2 == y:
                            occupied = True
                    if not occupied:
                        non_occupied_fields.append(x, y)
                    x = x + 20
                y = y + 20
        new_apple = non_occupied_fields[random.randint(0, len(non_occupied_fields) - 1)]
    return new_apple


# snake has definition only 16x16 pixels so it has to be shifted by 2 pixels up and right to stay middle
starting_coordinates = [random.randrange(22, play_field_width, 20), random.randrange(22, play_field__height, 20)]
# whole snake coordinates
snake_body = [starting_coordinates]
# apple coordinates
apple = generate_random_apple()
# used when we might have problem to put apple on a non occupied field, so at last stages of the game
non_occupied_fields = []
pyglet.app.run()
