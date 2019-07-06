from Game.agent import Agent
import pygame
from Game.ping_pong import PingPong
from Game import constants

ping_pong = PingPong()


def policy_gamers(state):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.time.delay(constants.TIME_DELAY)
    keys = pygame.key.get_pressed()
    ret_action_1, ret_action_2 = constants.NOTHING, constants.NOTHING
    if keys[pygame.K_UP]:
        ret_action_2 = constants.MOVE_UP
    if keys[pygame.K_DOWN]:
        ret_action_2 = constants.MOVE_DOWN
    if keys[pygame.K_w]:
        ret_action_1 = constants.MOVE_UP
    if keys[pygame.K_s]:
        ret_action_1 = constants.MOVE_DOWN
    if keys[pygame.K_ESCAPE]:
        ret_action_1 = constants.END_GAME
    return ret_action_1, ret_action_2


agent_1 = Agent(policy_gamers)
agent_2 = Agent(None)


while True:
    action_1 = constants.NOTHING
    action_2 = constants.NOTHING
    while action_1 != constants.END_GAME:
        action_1, action_2 = agent_1.get_action(None)
        reward = ping_pong.game_step(action_1, action_2)
        if reward[0]:
            ping_pong.reset()



