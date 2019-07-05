import pygame
from ball import Ball
from cart import Cart


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
        return self._cart_1.get_position(), \
               self._cart_2.get_position(), \
               self._ball.get_position(), \
               self._ball.get_direction()

    def auto_move(self):
        self._cart_1.get_position()[1] = self._ball.get_position()[1] - self._ball.get_radius()

    def step(self, actions):
        if actions[0] == 1:
            if self._cart_1.get_position()[1] > 0:
                self._cart_1.move_down()
        if actions[0] == 0:
            if self._cart_1.get_position()[1] <= self._window_size[1] - self._cart_1.get_size()[1]:
                self._cart_1.move_up()

        if actions[1] == 1:
            if self._cart_2.get_position()[1] > 0:
                self._cart_2.move_down()
        if actions[1] == 0:
            if self._cart_2.get_position()[1] <= self._window_size[1] - self._cart_2.get_size()[1]:
                self._cart_2.move_up()
        return self.get_reward()

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

        # if (self.ball.no_colision == 0):
        #
        #     # Если шар касается тележки
        #     if (self.cart_2.position[0] - self.ball.position[0] - self.ball.radius <= 0 and
        #             self.cart_2.position[0] + self.cart_2.size[0] / 2 - self.ball.position[0] - self.ball.radius > 0 and
        #             self.cart_2.position[1] - self.ball.position[1] < 0 and
        #             self.ball.position[1] - self.cart_2.position[1] - self.cart_2.size[1] < 0):
        #         self.ball.velocity_x = -1 * self.ball.velocity_x
        #         r2 += 1
        #         self.ball.no_colision = 20
        #
        #     if (self.cart_1.position[0] + self.cart_1.size[0] - self.ball.position[0] + self.ball.radius >= 0 and
        #             self.cart_1.position[0] + self.cart_1.size[0] / 2 - self.ball.position[0] + self.ball.radius < 0 and
        #             self.cart_1.position[1] - self.ball.position[1] < 0 and
        #             self.ball.position[1] - self.cart_1.position[1] - self.cart_1.size[1] < 0):
        #         self.ball.velocity_x = -1 * self.ball.velocity_x
        #         r += 1
        #         self.ball.no_colision = 20
        #
        #     # Если шар касается верхнего угла 2 тележки
        #     if (np.linalg.norm(np.subtract(self.cart_2.position, self.ball.position)) <= self.ball.radius and
        #             np.linalg.norm(np.subtract(self.cart_2.position, self.ball.position)) > self.ball.radius / 2 and
        #             self.cart_2.position[1] - self.ball.position[1] >= 0):
        #
        #         v1 = np.subtract(self.cart_2.position, self.ball.position)
        #         v2 = self.ball.velocity_x, self.ball.velocity_y
        #         angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        #         if (v1 / np.linalg.norm(v1))[1] < (v2 / np.linalg.norm(v2))[1]:
        #             angle *= -1
        #         self.ball.vel_turn(2 * angle)
        #         r2 += 1
        #         self.ball.no_colision = 20
        #
        #     # Если шар касается нижнего угла 2 тележки
        #     if (np.linalg.norm(np.subtract([self.cart_2.position[0], self.cart_2.position[1] + self.cart_2.size[1]],
        #                                    self.ball.position)) <= self.ball.radius and
        #             np.linalg.norm(np.subtract([self.cart_2.position[0], self.cart_2.position[1] + self.cart_2.size[1]],
        #                                        self.ball.position)) > self.ball.radius / 2 and
        #             self.ball.position[1] - self.cart_2.position[1] - self.cart_2.size[1] >= 0):
        #
        #         v1 = np.subtract([self.cart_2.position[0], self.cart_2.position[1] + self.cart_2.size[1]],
        #                          self.ball.position)
        #         v2 = self.ball.velocity_x, self.ball.velocity_y
        #         angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        #         if (v1 / np.linalg.norm(v1))[1] < (v2 / np.linalg.norm(v2))[1]:
        #             angle *= -1
        #         self.ball.vel_turn(2 * angle)
        #         r2 += 1
        #         self.ball.no_colision = 20
        #
        #     # Если шар касается верхнего угла 1 тележки
        #     if (np.linalg.norm(np.subtract([self.cart_1.position[0] + self.cart_1.size[0], self.cart_1.position[1]],
        #                                    self.ball.position)) <= self.ball.radius and
        #             np.linalg.norm(np.subtract([self.cart_1.position[0] + self.cart_1.size[0], self.cart_1.position[1]],
        #                                        self.ball.position)) > self.ball.radius / 2 and
        #             self.cart_1.position[1] - self.ball.position[1] >= 0):
        #
        #         v1 = np.subtract([self.cart_1.position[0] + self.cart_1.size[0], self.cart_1.position[1]],
        #                          self.ball.position)
        #         v2 = self.ball.velocity_x, self.ball.velocity_y
        #         angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        #         if (v1 / np.linalg.norm(v1))[1] > (v2 / np.linalg.norm(v2))[1]:
        #             angle *= -1
        #         self.ball.vel_turn(2 * angle)
        #         r += 1
        #         self.ball.no_colision = 20
        #
        #     # Если шар касается нижнего угла 1 тележки
        #     if (np.linalg.norm(np.subtract(
        #             [self.cart_1.position[0] + self.cart_1.size[0], self.cart_1.position[1] + self.cart_1.size[1]],
        #             self.ball.position)) <= self.ball.radius and
        #             np.linalg.norm(np.subtract(
        #                 [self.cart_1.position[0] + self.cart_1.size[0], self.cart_1.position[1] + self.cart_1.size[1]],
        #                 self.ball.position)) > self.ball.radius / 2 and
        #             self.ball.position[1] - self.cart_1.position[1] - self.cart_1.size[1] >= 0):
        #
        #         v1 = np.subtract(np.sum([self.cart_1.position, self.cart_1.size], axis=1), self.ball.position)
        #         v2 = self.ball.velocity_x, self.ball.velocity_y
        #         angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        #         if (v1 / np.linalg.norm(v1))[1] > (v2 / np.linalg.norm(v2))[1]:
        #             angle *= -1
        #         self.ball.vel_turn(2 * angle)
        #
        #         self.ball.velocity_x *= -1
        #         self.ball.velocity_y *= -1
        #
        #         r += 1
        #         self.ball.no_colision = 20
        # else:
        #     self.ball.no_colision -= 1
        #
        # # Отражение
        # if (ball_position[1] - ball_radius <= 0 or
        #         ball_position[1] + ball_radius >= self._window_size[1]):
        #     # изменить направление скорости по y
        #     self._ball.set_velocity_y(-1 * ball_velocity['y'])
        #
        # # Если шар касается сторон экрана для завершения
        # if (ball_position[0] <= 0 or
        #         ball_position[0] >= self._window_size[0]):
        #     # изменить направление скорости по y
        #     self._ball.set_velocity_y(-1 * ball_velocity['y'])
        #
        # self._ball.step()

        self._window.fill((0, 0, 0))
        # Заново рисуем тележку
        self._cart_1.draw()
        self._cart_2.draw()

        # Заново рисуем шар
        self._ball.draw()
        # Обновляем экран
        pygame.display.update()
        if action_1 != 0 and action_1 != 1 and action_2 != 0 and action_2 != 1:
            return self.get_reward()
        if action_1 == 1:
            if self._cart_1.get_position()[1] > 0:
                self._cart_1.move_down()
        elif action_1 == 0:
            if self._cart_1.get_position()[1] <= self._window_size[1] - self._cart_1.get_size()[1]:
                self._cart_1.move_up()

        if action_2 == 1:
            if self._cart_2.get_position()[1] > 0:
                self._cart_2.move_down()
        elif action_2 == 0:
            if self._cart_2.get_position()[1] <= self._window_size[1] - self._cart_2.get_size()[1]:
                self._cart_2.move_up()

        return self.get_reward()
