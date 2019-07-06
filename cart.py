import pygame
import constants


class Cart:
    def __init__(self, surface, position):
        self._velocity = constants.VELOCITY_CART
        self._size = [constants.WIDTH_CART, constants.HEIGHT_CART]
        self._position = position
        self._surface = surface
        self._color = constants.BLUE

    def draw(self):
        pygame.draw.rect(self._surface,
                         self._color,
                         pygame.Rect(self._position[0],
                                     self._position[1],
                                     self._size[0],
                                     self._size[1]))

    def set_position(self, position):
        self._position = position

    def move_up(self):
        self._position[1] -= self._velocity

    def move_down(self):
        self._position[1] += self._velocity

    def get_position(self):
        return self._position

    def get_size(self):
        return self._size
