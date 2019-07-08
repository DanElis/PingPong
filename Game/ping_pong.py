import pygame
import numpy as np
import math
from Game.ball import Ball
from Game.cart import Cart
from Game import constants


class PingPong:
    def __init__(self, visible=True):
        self._visible = visible
        pygame.init()
        self._r1 = 0
        self._r2 = 0
        self._window_size = constants.WIDTH_WINDOW, constants.HEIGHT_WINDOW
        self._window = None
        self._num_iteration = 1
        if self._visible:
            self._window = pygame.display.set_mode(self._window_size)
            pygame.display.set_caption('Ping Pong')
        self._cart_1 = Cart(self._window, [0, constants.HEIGHT_WINDOW / 2])
        self._cart_2 = Cart(self._window, [constants.WIDTH_WINDOW - constants.WIDTH_CART, constants.HEIGHT_WINDOW / 2])
        self._ball = Ball(self._window, [constants.WIDTH_WINDOW / 2, constants.HEIGHT_WINDOW / 2])

    def reset(self):
        self._cart_1 = Cart(self._window, [0, constants.HEIGHT_WINDOW / 2])
        self._cart_2 = Cart(self._window, [constants.WIDTH_WINDOW - constants.WIDTH_CART, constants.HEIGHT_WINDOW / 2])
        self._ball = Ball(self._window, [constants.WIDTH_WINDOW / 2, constants.HEIGHT_WINDOW / 2])
        self._num_iteration = 1
        return self.get_reward()

    def get_reward(self):
        if self.is_end_game():
            if self._ball.get_position()[0] <= 0:
                self._r1 += constants.LOSE_GAME
                self._r2 += constants.WIN_GAME
            elif self._ball.get_position()[0] >= self._window_size[0]:
                self._r1 += constants.WIN_GAME
                self._r2 += constants.LOSE_GAME
        if self._distance_from_ball(self._cart_1.get_position()[1]) > constants.HEIGHT_CART and self._num_iteration < 6:
            self._r1 -= self._distance_from_ball(self._cart_1.get_position()[1]) /math.factorial(self._num_iteration)
            self._r2 -= self._distance_from_ball(self._cart_2.get_position()[1])/math.factorial(self._num_iteration)
        return [*np.divide(self._cart_1.get_position(), self._window_size),
                *np.divide(self._cart_2.get_position(), self._window_size),
                *np.divide(self._ball.get_position(), self._window_size),
                self._ball.get_velocity()['x'] / (2 * self._ball.get_speed()) + 0.5,
                self._ball.get_velocity()['y'] / (2 * self._ball.get_speed()) + 0.5], \
               (self._r1, self._r2), \
               self.is_end_game()

    def _distance_from_ball(self, cart_position_y):
        return abs(cart_position_y - self._ball.get_position()[1])

    def is_end_game(self):
        return not (0 < self._ball.get_position()[0] < self._window_size[0])

    def redraw(self):
        self._window.fill((0, 0, 0))
        self._cart_1.draw()
        self._cart_2.draw()
        self._ball.draw()
        pygame.display.update()

    def perform_actions(self, action_1, action_2):
        if action_1 != constants.MOVE_DOWN and action_1 != constants.MOVE_UP and \
                action_2 != constants.MOVE_DOWN and action_2 != constants.MOVE_UP:
            return
        if action_1 == constants.MOVE_DOWN:
            if self._cart_1.get_position()[1] <= self._window_size[1] - self._cart_1.get_size()[1]:
                self._cart_1.move_down()
        elif action_1 == constants.MOVE_UP:
            if self._cart_1.get_position()[1] > 0:
                self._cart_1.move_up()

        if action_2 == constants.MOVE_DOWN:
            if self._cart_2.get_position()[1] <= self._window_size[1] - self._cart_2.get_size()[1]:
                self._cart_2.move_down()
        elif action_2 == constants.MOVE_UP:
            if self._cart_2.get_position()[1] > 0:
                self._cart_2.move_up()

    def game_step(self, action_1, action_2):

        self._r1 = 0
        self._r2 = 0

        if self._is_cart_1_touch():
            self._num_iteration += 1
            self._r1 += constants.REPEL
            self._reflection('x')

        if self._is_cart_2_touch():
            self._num_iteration += 1
            self._r2 += constants.REPEL
            self._reflection('x')

        if self._is_wall_touch():
            self._reflection('y')

        self._ball.step()

        self.perform_actions(action_1, action_2)

        if self._visible:
            self.redraw()
        return self.get_reward()

    def _is_cart_1_touch(self):
        ball_position = self._ball.get_position()
        ball_radius = 2 * self._ball.get_radius()
        cart_1_position = self._cart_1.get_position()
        cart_1_size = self._cart_1.get_size()
        return ball_position[0] - ball_radius - cart_1_size[0] <= 0 and \
               cart_1_position[1] < ball_position[1] < cart_1_position[1] + cart_1_size[1]

    def _is_cart_2_touch(self):
        ball_position = self._ball.get_position()
        ball_radius = 2 * self._ball.get_radius()
        cart_2_position = self._cart_2.get_position()
        cart_2_size = self._cart_2.get_size()
        return ball_position[0] + ball_radius + cart_2_size[0] >= self._window_size[0] and \
               cart_2_position[1] < ball_position[1] < cart_2_position[1] + cart_2_size[1]

    def _is_wall_touch(self):
        ball_position = self._ball.get_position()
        ball_radius = 2 * self._ball.get_radius()
        return ball_position[1] - ball_radius <= 0 or ball_position[1] + ball_radius >= self._window_size[1] or \
               ball_position[0] <= 0 or ball_position[0] >= self._window_size[0]

    def _reflection(self, direction):
        if direction == 'x':
            self._ball.set_velocity_x(-1 * self._ball.get_velocity()['x'])
        elif direction == 'y':
            self._ball.set_velocity_y(-1 * self._ball.get_velocity()['y'])

    def quit(self):
        pygame.quit()

    def set_visible(self, visible):
        if visible and not self._visible:
            self._window = pygame.display.set_mode(self._window_size)
            pygame.display.set_caption('Ping Pong')
            self._cart_1 = Cart(self._window, [0, constants.HEIGHT_WINDOW / 2])
            self._cart_2 = Cart(self._window, [constants.WIDTH_WINDOW - constants.WIDTH_CART, constants.HEIGHT_WINDOW / 2])
            self._ball = Ball(self._window, [constants.WIDTH_WINDOW / 2, constants.HEIGHT_WINDOW / 2])
        self._visible = visible
