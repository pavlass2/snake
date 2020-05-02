#!/usr/bin/python

import os
import pyglet


class ImgProvider:
    def __init__(self, path='img'):
        self.snake_img = pyglet.image.load(os.path.join('img', 'snake.png'))
        self.apple_img = pyglet.image.load(os.path.join('img', 'apple.png'))
        self.wall_img = pyglet.image.load(os.path.join('img', 'wall.png'))
