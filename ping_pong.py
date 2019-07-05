import pygame
from ball import Ball
from cart import Cart

NOTHING = 2
END_GAME = -1
MOVE_DOWN = 1
MOVE_UP = 0


class PingPong:
    def __init__(self):
        pygame.init()
        self._window_size = 500, 500
        self._window = pygame.display.set_mode(self._window_size)
        pygame.display.set_caption('Ping Pong')
        self._cart_1 = Cart(self._window, [0, 250])
        self._cart_2 = Cart(self._window, [490, 250])
        self._ball = Ball(self._window, [250, 250])

    def reset(self):
        self._cart_1 = Cart(self._window, [0, 250])
        self._cart_2 = Cart(self._window, [490, 250])
        self._ball = Ball(self._window, [250, 250])

    def get_reward(self):
        return self.is_end_game(), \
               self._cart_1.get_position(), \
               self._cart_2.get_position(), \
               self._ball.get_position(), \
               self._ball.get_direction()

    def auto_move(self):
        self._cart_1.get_position()[1] = self._ball.get_position()[1] - self._ball.get_radius()

    # def step(self, actions):
    #     if actions[0] == 1:
    #         if self._cart_1.get_position()[1] > 0:
    #             self._cart_1.move_down()
    #     if actions[0] == 0:
    #         if self._cart_1.get_position()[1] <= self._window_size[1] - self._cart_1.get_size()[1]:
    #             self._cart_1.move_up()
    #
    #     if actions[1] == 1:
    #         if self._cart_2.get_position()[1] > 0:
    #             self._cart_2.move_down()
    #     if actions[1] == 0:
    #         if self._cart_2.get_position()[1] <= self._window_size[1] - self._cart_2.get_size()[1]:
    #             self._cart_2.move_up()
    #     return self.get_reward()

    def is_end_game(self):
        return not (0 < self._ball.get_position()[0] < self._window_size[0])

    def game_step(self, action_1, action_2):

        # Если шар касается тележки #Поменяй шар на квадрат, иначе придется тут переписать
        cart_1_position = self._cart_1.get_position()
        cart_2_position = self._cart_2.get_position()
        ball_position = self._ball.get_position()
        ball_radius = self._ball.get_radius()
        cart_2_size = self._cart_2.get_size()
        cart_1_size = self._cart_1.get_size()
        ball_velocity = self._ball.get_velocity()

        if (cart_2_position[0] - ball_position[0] - ball_radius <= 0 and
                cart_2_position[0] + cart_2_size[0] / 2 - ball_position[0] - ball_radius > 0 and
                cart_2_position[1] - ball_position[1] < ball_radius / 1.5 and
                ball_position[1] - cart_2_position[1] - cart_2_size[1] < ball_radius / 1.5 or
                cart_1_position[0] + cart_1_size[0] - ball_position[0] + ball_radius >= 0 and
                cart_1_position[0] + cart_1_size[0] / 2 - ball_position[0] + ball_radius < 0 and
                cart_1_position[1] - ball_position[1] < ball_radius / 1.5 and
                ball_position[1] - cart_1_position[1] - cart_1_size[1] < ball_radius / 1.5):
            self._ball.set_velocity_x(-1 * ball_velocity['x'])

        # Отражение
        if (ball_position[1] - ball_radius <= 0 or
                ball_position[1] + ball_radius >= self._window_size[1]):
            # изменить направление скорости по y
            self._ball.set_velocity_y(-1 * ball_velocity['y'])

        # Если шар касается сторон экрана для завершения
        if (ball_position[0] <= 0 or
                ball_position[0] >= self._window_size[0]):
            # изменить направление скорости по y
            self._ball.set_velocity_y(-1 * ball_velocity['y'])

        self._ball.step()

        self._window.fill((0, 0, 0))
        # Заново рисуем тележку
        self._cart_1.draw()
        self._cart_2.draw()

        # Заново рисуем шар
        self._ball.draw()
        # Обновляем экран
        pygame.display.update()
        if action_1 != MOVE_DOWN and action_1 != MOVE_UP and action_2 != MOVE_DOWN and action_2 != MOVE_UP:
            return self.get_reward()
        if action_1 == MOVE_DOWN:
            if self._cart_1.get_position()[1] > 0:
                self._cart_1.move_down()
        elif action_1 == MOVE_UP:
            if self._cart_1.get_position()[1] <= self._window_size[1] - self._cart_1.get_size()[1]:
                self._cart_1.move_up()

        if action_2 == MOVE_DOWN:
            if self._cart_2.get_position()[1] > 0:
                self._cart_2.move_down()
        elif action_2 == MOVE_UP:
            if self._cart_2.get_position()[1] <= self._window_size[1] - self._cart_2.get_size()[1]:
                self._cart_2.move_up()

        return self.get_reward()
