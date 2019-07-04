#!/usr/bin/env python
# coding: utf-8

# In[406]:


#!pip install pygame


# In[407]:


import pygame
#from ball import Ball
#from cart import Cart
#from agent import Agent


# In[408]:


import random
import math
#Класс мяча
class Ball:
    def __init__(self, surface, position):
        self.radius = 20 
        self.surface = surface
        self.position = position
        self.speed = 4
        
        angle = random.randint(-45, 45) + random.randint(0, 1) * 180
        
        self.velocity_x = self.speed * math.cos(angle * math.pi / 180)
        self.velocity_y = self.speed * math.sin(angle * math.pi / 180)
        
        self.color = (255,0,0) #Красный

    def draw(self):  
        pygame.draw.circle(self.surface, 
                           self.color, 
                           (int(self.position[0]), int(self.position[1])), 
                           self.radius)

    def set_Position(self, position):
        self.position = position
        
        angle = random.randint(-45, 45) + random.randint(0, 1) * 180
        
        self.velocity_x = self.speed * math.cos(angle * math.pi / 180)
        self.velocity_y = self.speed * math.sin(angle * math.pi / 180)


# In[409]:


#Класс тележки
class Cart:
    def __init__(self, surface, position):
        self.velocity = 5
        self.size = [10, 50] 
        self.position = position
        self.surface = surface
        self.color = (0,255,0) 
    
    def draw(self): 
        pygame.draw.rect(self.surface, 
                         self.color, 
                         pygame.Rect(self.position[0],  
                                     self.position[1], 
                                     self.size[0], 
                                     self.size[1]))
    def set_Position(self, position):
        self.position = position

    def move_up(self):
        if self.position[1] <= window_size[1] - self.size[1]:
            self.position[1] += self.velocity
    def move_down(self):
        if self.position[1] > 0:
            self.position[1] -= self.velocity


# In[410]:


#Класс вирутального игрока
class Agent():
    def __init__(self, cart):
        self.cart = cart
        self.last = self.cart.move_up
        self.n = -1
    #Алгоритм случайной игры    
    def auto_play(self):
        if self.n > 0:
            self.n -= 1
        else:
            self.n = 20
            if ball.position[1] > self.cart.position[1]:
                self.last = random.choice((self.cart.move_up, self.cart.move_down, self.cart.move_up, self.cart.move_up))
            else:
                self.last = random.choice((self.cart.move_up, self.cart.move_down, self.cart.move_down, self.cart.move_down))
        self.last()                          


# In[411]:


# Функция получения текущей ситуации на игровом поле
def get_obs(cart_1, cart_2, ball):
    return (cart_1.position, cart_2.position, ball.position, ball.direction)


# In[412]:


#Автоигра
def auto_move(ball, cart):
    cart.position[1] = ball.position[1] - ball.radius


# In[413]:


pygame.init()
window_size = 500, 500 
window = pygame.display.set_mode(window_size)
pygame.display.set_caption('Ping Pong')

#Создаю тележки
cart_1 = Cart(window, [0, 250]) 
cart_2 = Cart(window, [490, 250])
#Создаю мяч
ball = Ball(window, [250, 250])

#Создаю агента
agent = Agent(cart_2)

#Рисую мяч и тележки
cart_1.draw()
cart_2.draw()
ball.draw()
pygame.display.update()


# In[414]:


def game_cicle():
    game = True
    #Цикл игры
    while game:
        #Чтобы не так быстро
        pygame.time.delay(10)
        #Обработка событий
        for event in pygame.event.get():
            #Выход
            if event.type == pygame.QUIT:
                game = False
                pygame.quit()

        #Какие кнопки нажаты
        keys = pygame.key.get_pressed()
        #Если нажата вверх
        if keys[pygame.K_UP]:
            #Проверка на выход за границы
            cart_1.move_down()
        #Если нажата вниз
        if keys[pygame.K_DOWN]:
            #Проверка на выход за границы
            cart_1.move_up()
        #Если нажата W
        if keys[pygame.K_w]:
            #Проверка на выход за границы
            cart_2.move_down()
        #Если нажата S
        if keys[pygame.K_s]:
            #Проверка на выход за границы
            cart_2.move_up()
        if keys[pygame.K_ESCAPE]:
                game = False
                pygame.quit()
        
        #Если шар касается тележки #Поменяй шар на квадрат, иначе придется тут переписать      
        if (cart_2.position[0] - ball.position[0] - ball.radius <= 0 and cart_2.position[0] + cart_2.size[0]/2 - ball.position[0] - ball.radius > 0 and 
            cart_2.position[1] - ball.position[1] < ball.radius / 1.5 and ball.position[1] - cart_2.position[1] - cart_2.size[1] < ball.radius / 1.5 or
            cart_1.position[0] + cart_1.size[0] - ball.position[0] + ball.radius >= 0 and cart_1.position[0] + cart_1.size[0]/2 - ball.position[0] + ball.radius < 0 and
            cart_1.position[1] - ball.position[1] < ball.radius / 1.5 and ball.position[1] - cart_1.position[1] - cart_1.size[1] < ball.radius / 1.5):
            ball.velocity_x = -1 * ball.velocity_x
            
        #Отражение
        if (ball.position[1] - ball.radius <= 0 or 
            ball.position[1] + ball.radius >= window_size[1]):
            # изменить направление скорости по y
            ball.velocity_y = -1 * ball.velocity_y 
        
        
        #Если шар касается сторон экрана для завершения
        if (ball.position[0] <= 0 or 
            ball.position[0] >= window_size[0]):
            # изменить направление скорости по y
            ball.velocity_y = -1 * ball.velocity_y 
            game = False

        #Это чисто для отладки
        #if (ball.position[0] + ball.radius >= window_size[0]):
            # изменить направление скорости по x
            #ball.velocity_x = -1 * ball.velocity_x
            #game = False


        #Переместить шар
        ball.position[0] += ball.velocity_x
        ball.position[1] += ball.velocity_y 

        #auto_move(ball, cart_2)
        agent.auto_play()

        #Очистка экрана
        window.fill((0,0,0))
        #Заново рисуем тележку
        cart_1.draw()   
        cart_2.draw()

        #Заново рисуем шар
        ball.draw()
        #Обновляем экран
        pygame.display.update()


# In[415]:


while True:
    game_cicle()
    cart_1.set_Position([0, 250])    
    cart_2.set_Position([490, 250])
    ball.set_Position([250,250])
pygame.quit()


# In[ ]:




