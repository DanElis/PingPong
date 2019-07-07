import math
import random
import pygame

from Game import constants


class Ball:
    def __init__(self, surface, position):
        self._radius = constants.RADIUS_BALL
        if surface is not None:
            self._surface = surface
        self._position = position
        self._speed = constants.BALL_SPEED

        angle = random.randint(-45, 45) + random.randint(0, 1) * 180

        self._velocity_x = self._speed * math.cos(angle * math.pi / 180)
        self._velocity_y = self._speed * math.sin(angle * math.pi / 180)

        self._color = constants.RED

    def draw(self):
        pygame.draw.circle(self._surface,
                           self._color,
                           (int(self._position[0]), int(self._position[1])),
                           self._radius)

    def get_position(self):
        return self._position

    def set_position(self, new_position):
        self._position = new_position

    def reset_position(self, position):
        self._position = position

        angle = random.randint(-45, 45) + random.randint(0, 1) * 180

        self._velocity_x = self._speed * math.cos(angle * math.pi / 180)
        self._velocity_y = self._speed * math.sin(angle * math.pi / 180)

    def get_direction(self):
        return [self._velocity_x, self._velocity_y]

    def get_radius(self):
        return self._radius

    def get_velocity(self):
        return {'x': self._velocity_x,
                'y': self._velocity_y}

    def set_velocity_x(self, new_velocity_x):
        self._velocity_x = new_velocity_x

    def set_velocity_y(self, new_velocity_y):
        self._velocity_y = new_velocity_y

    def step(self):
        self._position[0] += self._velocity_x
        self._position[1] += self._velocity_y

    def get_speed(self):
        return self._speed

    def set_speed(self, new_speed):
        self._speed = new_speed