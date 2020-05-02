#!/usr/bin/python
import json
import pyglet
import random
import logger
import keyCash
import menu
import imgProvider

# WINDOW
# controls game speed by frame rate, default is 10
game_speed = None

# width of whole window
window_width = None

# height of whole window
window_height = None


def load_options():
    global window_width
    global window_height
    global game_speed
    try:
        with open("options.json") as json_file:
            options = json.load(json_file)
            for option in options["options"]:
                window_width = option["window_width"]
                window_height = option["window_height"]
                game_speed = option["game_speed"]
    except FileNotFoundError:
        logger.log_debug("File: options.json was not found. Switching options to default.")
        game_speed = 12
        window_width = 1060
        window_height = 480


# width of area where score, time and more are showed
score_area_width = 100

# main window
load_options()
window = pyglet.window.Window(window_width, window_height)

play_field_height = None
play_field_width = None
fields = None

# RUN CONTROL
# game stops if this is true
game_over = False

# is snake moving
game_running = False

# is game in progress (but snake is not necessarily moving)
game_in_progress = False

# takes care of logging
logger = logger.Logger()

# takes care of user input and its usage
key_cash = keyCash.KeyCash()

# provides images
img_provider = imgProvider.ImgProvider()

# MENUS
# controls if to show main menu
show_main_menu = True
# main menu
main_menu = None

# controls if to show pause menu
show_pause_menu = False
# pause menu
pause_menu = None

# controls if to show options menu
show_options_menu = False
# options menu accessible from main menu
options_menu = None

# controls if to show game speed options menu
show_game_speed_options_menu = False
# game speed options menu accessible from main menu
game_speed_options_menu = None

# controls if to show layout options menu
show_layout_options_menu = False
# layout options menu accessible from options menu
layout_options_menu = None

# layout variables
full_width = 1060
half_width = 580
full_height = 960
half_height = 480

# speed variables
normal_speed = 10
fast_speed = 12
very_fast_speed = 14
crazy_speed = 16


def initialize():
    global main_menu
    global pause_menu
    global options_menu
    global game_speed_options_menu
    # global game_over_menu
    global layout_options_menu
    global window_height
    global window_width
    global play_field_height
    global play_field_width
    global fields

    # main menu
    main_menu = menu.Menu(img_provider,
                          ["New game", "Options", "Exit"],
                          window_height,
                          window_width)

    # pause menu
    pause_menu = menu.Menu(img_provider,
                           ["Continue", "New game", "Back to main menu", "Exit snake"],
                           window_height,
                           window_width)

    # options menu accessible from main menu
    options_menu = menu.Menu(img_provider,
                             ["Layout (" + get_layout_in_text() + ")",
                              "Game speed (" + get_game_speed_in_text() + ")",
                              "Go back"],
                             window_height,
                             window_width)

    # game speed options menu accessible from options menu
    game_speed_options_menu = menu.Menu(img_provider,
                                        ["Normal", "Fast", "Very Fast", "Crazy", "Cancel"],
                                        window_height,
                                        window_width)

    # layout options menu accessible from options menu
    layout_options_menu = menu.Menu(img_provider,
                                    ["Square", "Horizontal", "Vertical", "Cancel"],
                                    window_height,
                                    window_width)

    # maximum width where snake can move counted in pixels - that is width minus right side wall
    play_field_width = window_width - score_area_width

    # maximum height where snake can move counted in pixels - that is height minus top side wall
    play_field_height = window_height - 20

    # sum of all possible positions snake's head can use
    fields = play_field_height * play_field_width / 20


# after window is opened, this is done
# and then every time the snake moves
@window.event
def on_draw():
    batch = pyglet.graphics.Batch()
    sprites = []

    if game_running:
        global game_over
        global snake_body
        global score_area_width
        global play_field_height
        if game_over:
            # freeze_draw = True
            label_position_x = play_field_width / 2
            label_position_y = play_field_height / 2 + play_field_height // 10
            sprites.append(pyglet.text.Label("Game over",
                                             font_name='Times New Roman',
                                             font_size=28,
                                             x=label_position_x, y=label_position_y,
                                             anchor_x='center', anchor_y='center',
                                             batch=batch))

            sprites.append(pyglet.text.Label("Press space to return to menu or escape to exit",
                                             font_name='Times New Roman',
                                             font_size=12,
                                             x=label_position_x, y=label_position_y - 50,
                                             anchor_x='center', anchor_y='center',
                                             batch=batch))
        else:
            # snake sprites
            window.clear()
            for num, snake_part in enumerate(snake_body):
                sprite = pyglet.sprite.Sprite(img_provider.snake_img, batch=batch)
                sprite.x = snake_part[0]
                sprite.y = snake_part[1]
                sprites.append(sprite)

                # fill empty space in snakes body
                if num + 1 < len(snake_body):
                    sprite_filling = pyglet.sprite.Sprite(img_provider.snake_img, batch=batch)
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
                sprite = pyglet.sprite.Sprite(img_provider.wall_img, batch=batch)
                sprite.x = counter
                sprite.y = window_height - 20
                sprites.append(sprite)

                sprite = pyglet.sprite.Sprite(img_provider.wall_img, batch=batch)
                sprite.x = counter
                sprite.y = 0
                sprites.append(sprite)

                counter = counter + 20
            # vertical
            # global score_area_width
            counter = 0
            while counter < play_field_height:
                sprite = pyglet.sprite.Sprite(img_provider.wall_img, batch=batch)
                sprite.x = play_field_width
                sprite.y = counter
                sprites.append(sprite)

                sprite = pyglet.sprite.Sprite(img_provider.wall_img, batch=batch)
                sprite.x = 0
                sprite.y = counter
                sprites.append(sprite)
                counter = counter + 20

            # apple sprite
            apple_sprite = pyglet.sprite.Sprite(img_provider.apple_img, batch=batch)
            new_apple_coordinates = apple
            apple_sprite.x = new_apple_coordinates[0]
            apple_sprite.y = new_apple_coordinates[1]
            sprites.append(apple_sprite)
    elif show_pause_menu:
        window.clear()
        pause_menu.batch_menu(batch, sprites)
    elif show_options_menu:
        window.clear()
        options_menu.batch_menu(batch, sprites)
    elif show_game_speed_options_menu:
        window.clear()
        game_speed_options_menu.batch_menu(batch, sprites)
    elif show_layout_options_menu:
        window.clear()
        layout_options_menu.batch_menu(batch, sprites)
    else:
        window.clear()
        main_menu.batch_menu(batch, sprites)
    batch.draw()


# every time user presses key do this
@window.event
def on_key_press(symbol, modifiers):
    global show_main_menu
    global show_pause_menu
    global show_options_menu
    global show_game_speed_options_menu
    global show_layout_options_menu
    global game_running
    global game_in_progress
    global game_speed

    # managing key input for game play
    if game_running and not game_over:
        if symbol == pyglet.window.key.LEFT or symbol == pyglet.window.key.RIGHT or symbol == pyglet.window.key.UP or symbol == pyglet.window.key.DOWN:
            if not game_in_progress:
                pyglet.clock.schedule_interval(movement, 1 / game_speed)
                game_running = True
                game_in_progress = True
            key_cash.add_command(symbol)
        elif symbol == pyglet.window.key.ESCAPE:
            game_running = False
            show_pause_menu = True
            window.clear()
            return pyglet.event.EVENT_HANDLED

    # main menu input logic
    elif show_main_menu:
        if symbol == pyglet.window.key.LEFT or symbol == pyglet.window.key.UP:
            main_menu.select_item(-1)
        elif symbol == pyglet.window.key.RIGHT or symbol == pyglet.window.key.DOWN:
            main_menu.select_item(1)
        elif symbol == pyglet.window.key.ENTER or symbol == pyglet.window.key.SPACE:
            selected_index = main_menu.get_selected_index()
            if selected_index == 0:
                run_game()
            elif selected_index == 1:
                show_main_menu = False
                show_options_menu = True
            elif selected_index == 2:
                pyglet.clock.unschedule(movement)
                window.close()

    # pause menu input logic
    elif show_pause_menu:
        if symbol == pyglet.window.key.LEFT or symbol == pyglet.window.key.UP:
            pause_menu.select_item(-1)
        elif symbol == pyglet.window.key.RIGHT or symbol == pyglet.window.key.DOWN:
            pause_menu.select_item(1)
        elif symbol == pyglet.window.key.ENTER or symbol == pyglet.window.key.SPACE:
            selected_index = pause_menu.get_selected_index()
            if selected_index == 0:
                run_game()
            elif selected_index == 1:
                reset()
                run_game()
            elif selected_index == 2:
                reset()
                show_pause_menu = False
                show_main_menu = True
            elif selected_index == 3:
                pyglet.clock.unschedule(movement)
                window.close()

    # options menu input logic
    elif show_options_menu:
        if symbol == pyglet.window.key.LEFT or symbol == pyglet.window.key.UP:
            options_menu.select_item(-1)
        elif symbol == pyglet.window.key.RIGHT or symbol == pyglet.window.key.DOWN:
            options_menu.select_item(1)
        elif symbol == pyglet.window.key.ENTER or symbol == pyglet.window.key.SPACE:
            selected_index = options_menu.get_selected_index()
            if selected_index == 0:
                show_options_menu = False
                show_layout_options_menu = True
            elif selected_index == 1:
                show_options_menu = False
                show_game_speed_options_menu = True
            elif selected_index == 2:
                show_options_menu = False
                show_main_menu = True
        elif symbol == pyglet.window.key.ESCAPE or symbol == pyglet.window.key.BACKSPACE:
            show_options_menu = False
            show_main_menu = True
            options_menu.reset_index()
            return pyglet.event.EVENT_HANDLED

    # game speed options input menu logic
    elif show_game_speed_options_menu:
        if symbol == pyglet.window.key.LEFT or symbol == pyglet.window.key.UP:
            game_speed_options_menu.select_item(-1)
        elif symbol == pyglet.window.key.RIGHT or symbol == pyglet.window.key.DOWN:
            game_speed_options_menu.select_item(1)
        elif symbol == pyglet.window.key.ENTER or symbol == pyglet.window.key.SPACE:
            selected_index = game_speed_options_menu.get_selected_index()
            if selected_index == 0:
                game_speed = 10
                initialize()
                save_options()
            elif selected_index == 1:
                game_speed = 12
                initialize()
                save_options()
            elif selected_index == 2:
                game_speed = 14
                initialize()
                save_options()
            elif selected_index == 3:
                game_speed = 16
                initialize()
                save_options()
            show_game_speed_options_menu = False
            show_options_menu = True
        elif symbol == pyglet.window.key.ESCAPE or symbol == pyglet.window.key.BACKSPACE:
            show_game_speed_options_menu = False
            show_options_menu = True
            game_speed_options_menu.reset_index()
            return pyglet.event.EVENT_HANDLED

    # layout options input menu
    elif show_layout_options_menu:
        if symbol == pyglet.window.key.LEFT or symbol == pyglet.window.key.UP:
            layout_options_menu.select_item(-1)
        elif symbol == pyglet.window.key.RIGHT or symbol == pyglet.window.key.DOWN:
            layout_options_menu.select_item(1)
        elif symbol == pyglet.window.key.ENTER or symbol == pyglet.window.key.SPACE:
            selected_index = layout_options_menu.get_selected_index()
            if selected_index == 0:
                set_window_size(full_width, full_height)
                save_options()
            elif selected_index == 1:
                set_window_size(full_width, half_height)
                save_options()
            elif selected_index == 2:
                set_window_size(half_width, full_height)
                save_options()
            show_layout_options_menu = False
            show_options_menu = True
        elif symbol == pyglet.window.key.ESCAPE or symbol == pyglet.window.key.BACKSPACE:
            show_game_speed_options_menu = False
            show_options_menu = True
            game_speed_options_menu.reset_index()
            return pyglet.event.EVENT_HANDLED

    # after death input
    elif game_over:
        if symbol == pyglet.window.key.ENTER or symbol == pyglet.window.key.SPACE:
            show_main_menu = True
            game_running = False
            reset()


def set_window_size(width, height):
    global window_width
    global window_height
    window_width = width
    window_height = height
    window.set_size(window_width, window_height)
    initialize()
    reset()


# calculate the movement
def movement(dt):
    if game_running and not game_over:
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
            or (y > play_field_height - 18) \
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
    global game_in_progress
    global key_cash
    pyglet.clock.unschedule(movement)
    game_over = True
    game_in_progress = False
    key_cash = keyCash.KeyCash()
    logger.log_debug("Hit")


# returns array of random 2D coordinates [x, y] in play field thar are not occupied by snake
def generate_random_apple():
    global fields
    global snake_body
    new_apple = None
    # first half of the game
    if len(snake_body) < fields / 0.05:
        while not new_apple:
            suggested_coordinates = [random.randrange(20, play_field_width, 20),
                                     random.randrange(20, play_field_height, 20)]
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
            while y <= play_field_height:
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


def reset():
    global key_cash
    global snake_body
    global non_occupied_fields
    global apple
    global game_over
    global show_pause_menu
    global game_in_progress
    key_cash.reset()
    snake_body = []
    shuffle_starting_coordinates()
    non_occupied_fields = []
    apple = generate_random_apple()
    game_over = False
    show_pause_menu = False
    game_in_progress = False
    pyglet.clock.unschedule(movement)


def shuffle_starting_coordinates():
    # snake has definition only 16x16 pixels so it has to be shifted by 2 pixels up and right to stay middle
    global snake_body
    starting_coordinates = [random.randrange(22, play_field_width, 20), random.randrange(22, play_field_height, 20)]
    snake_body = [starting_coordinates]


def run_game():
    global show_main_menu
    show_main_menu = False

    global show_pause_menu
    show_pause_menu = False

    global show_options_menu
    show_options_menu = False

    global show_game_speed_options_menu
    show_game_speed_options_menu = False

    global show_layout_options_menu
    show_layout_options_menu = False

    global game_running
    game_running = True


def get_layout_in_text():
    if window_width == full_width and window_height == full_height:
        return "Square"
    elif window_width == full_width and window_height == half_height:
        return "Horizontal"
    elif window_width == half_width and window_height == full_height:
        return "Vertical"
    else:
        return str(window_width) + "x" + str(window_height)


def get_game_speed_in_text():
    if game_speed == normal_speed:
        return "Normal"
    elif game_speed == fast_speed:
        return "Fast"
    elif game_speed == very_fast_speed:
        return "Very fast"
    elif game_speed == crazy_speed:
        return "Crazy"
    else:
        return game_speed


def save_options():
    options = {"options": []}
    options["options"].append({
        "window_width": window_width,
        "window_height": window_height,
        "game_speed": game_speed
    })
    with open('options.json', 'w') as outfile:
        json.dump(options, outfile)


initialize()
# snake has definition only 16x16 pixels so it has to be shifted by 2 pixels up and right to stay middle
# whole snake coordinates are kept here
snake_body = []
shuffle_starting_coordinates()
# apple coordinates
apple = generate_random_apple()
# used when we might have problem to put apple on a non occupied field, so at last stages of the game
non_occupied_fields = []
pyglet.app.run()
logger.log_debug("PROGRAM EXIT")
