#!/usr/bin/python

import pyglet


class Menu:
    def __init__(self,
                 img_provider,
                 menu_items,
                 window_height,
                 window_width,
                 title=None,
                 color=(255, 255, 255, 255),
                 selection_color=(34, 226, 53, 255),
                 selected_item=0):
        self.__img_provider = img_provider
        self.__menu_items = menu_items
        self.__window_height = window_height
        self.__window_width = window_width
        self.__title = title
        self.__color = color
        self.__selection_color = selection_color
        self.__font_size = 20
        self.__height_coefficient = window_height / len(menu_items)
        self.__icon_horizontal_position = (window_width // 2) - window_width / 5
        self.__vertical_center = window_height // 2
        self.__selected_item = selected_item
        self.__index_iteration_check()

    # prepares menu into batch
    def batch_menu(self, batch, sprites):
        # calculate height in which to place menu
        height = self.__vertical_center + self.__font_size * len(self.__menu_items) / 2

        # append title if there is any
        if self.__title:
            sprites.append(pyglet.text.Label(self.__title,
                                             color=self.__color,
                                             font_name='Times New Roman',
                                             font_size=self.__font_size + 16,
                                             x=self.__window_width / 2,
                                             y=height + self.__calculate_height_shift(height),
                                             anchor_x='center',
                                             anchor_y='center',
                                             batch=batch))

        # append menu items
        for i, menu_item in enumerate(self.__menu_items):
            color = self.__color
            # color selected menu item
            if i == self.__selected_item:
                color = self.__selection_color
                sprite = pyglet.sprite.Sprite(self.__img_provider.snake_img, batch=batch)
                sprite.x = self.__icon_horizontal_position
                sprite.y = height - 10
                sprites.append(sprite)

            sprites.append(pyglet.text.Label(menu_item, color=color, font_name='Times New Roman',
                                             font_size=self.__font_size, x=self.__window_width / 2, y=height,
                                             anchor_x='center', anchor_y='center', batch=batch))
            height -= self.__calculate_height_shift(height)

    def select_item(self, index_movement):
        self.__selected_item += index_movement
        self.__index_iteration_check()

    def get_selected_index(self):
        result = self.__selected_item
        # after selection is used, reset index
        self.reset_index()
        return result

    def reset_index(self):
        self.__selected_item = 0

    # Keeps index in bounds
    def __index_iteration_check(self):
        if self.__selected_item > len(self.__menu_items) - 1:
            self.__selected_item = 0
        elif self.__selected_item < 0:
            self.__selected_item = len(self.__menu_items) - 1

    # calculates height of next menu item based on total amount of menu items
    def __calculate_height_shift(self, height):
        if len(self.__menu_items) < 4:
            return self.__height_coefficient / 5
        elif len(self.__menu_items) == 4:
            return self.__height_coefficient / 4
        else:
            return self.__height_coefficient / 3