from agent import Agent
import pygame
from ping_pong import PingPong
NOTHING = 2
END_GAME = -1


ping_pong = PingPong()


def policy_gamers(state):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.time.delay(10)
    pygame.time.delay(10)
    keys = pygame.key.get_pressed()
    ret_action_1, ret_action_2 = NOTHING, NOTHING
    if keys[pygame.K_UP]:
        ret_action_1 = 1
    if keys[pygame.K_DOWN]:
        ret_action_1 = 0
    if keys[pygame.K_w]:
        ret_action_2 = 1
    if keys[pygame.K_s]:
        ret_action_2 = 0
    if keys[pygame.K_ESCAPE]:
        ret_action_1 = END_GAME
    return ret_action_1, ret_action_2


agent_1 = Agent([0, 1], policy_gamers())
agent_2 = Agent([0, 1], None)


while True:
    action_1 = NOTHING
    action_2 = NOTHING
    while action_1 != END_GAME:
        action_1, action_2 = agent_1.get_action(None)
        ping_pong.game_step(action_1, action_2)



