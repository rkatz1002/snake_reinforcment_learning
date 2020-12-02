import pygame
import random
from math import sqrt
import numpy as np

# based on:
# https://www.edureka.co/blog/snake-game-with-pygame/

import gym
from gym import spaces


class Snake_game(gym.Env):
    
    #pygame display conigurations
    pygame.display.set_caption('Snake Game Reinforcment Learning')
    clock = pygame.time.Clock()
    white = (255, 255, 255)
    yellow = (255, 255, 102)
    black = (0, 0, 0)
    red = (213, 50, 80)
    green = (0, 255, 0)
    blue = (50, 153, 213)
    dis_width = 600
    dis_height = 400
    font_style = None
    score_font = None
    snake_block = 10
    snake_speed = 25
    dis = pygame.display.set_mode((dis_width, dis_height))
    
    #snake configurations
    x1 = dis_width / 2     #x position
    y1 = dis_height / 2    #y position
    snake_Head=[x1, y1]    #head array
    snake_List=[]          #snake list
    Length_of_snake=1      #length of snake
    direction=0            #snake direction (starts as left==0)

    #rewards
    reward_eat_food = 0.5
    reward_loose = -1
    reward_do_nothing = 0.01
    reward_do_nothing_go_further_away= -0.2

    #gym env configs
    action_space = spaces.Discrete(3)
    observation_space = spaces.MultiDiscrete(
        [2, 2, 2, 2, 2, 2, 4]
    ) 

    def __init__(self):
        """
            starts enviornment.
        """

        self.snake_List = []
        self.Length_of_snake = 1
        self.direction=0

        self.foodx = round(random.randrange(0, self.dis_width-10) / 10.0) * 10.0
        self.foody = round(random.randrange(0, self.dis_height-10) / 10.0) * 10.0

        pygame.init()
        self.font_style = pygame.font.SysFont("comicsansms", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)
        

    ####################
    ##HELPER FUNCTIONS##
    ####################

    def update_score(self, score):

        """
            updates score on game screen.
        """

        value = self.score_font.render("Your Score: " + str(score), True, self.yellow)
        self.dis.blit(value, [0, 0])

    def draw_snake(self, snake_block):
        """
            draws snake on game screen
        """
        for x in self.snake_List:
            pygame.draw.rect(self.dis, self.black, [x[0], x[1], snake_block, snake_block])
    
    def message(self, msg, color):
        """
            Shows message on game screen.
        """

        mesg = self.font_style.render(msg, True, color)
        self.dis.blit(mesg, [self.dis_width / 6, self.dis_height / 3])

    def map_type_to_val(self, reward_type):
        if reward_type==1:
            return self.reward_eat_food
        
        elif reward_type==2:
            return self.reward_loose
            
        elif reward_type==3:
            return self.reward_do_nothing

        elif reward_type==4:
            return self.reward_do_nothing_go_further_away
    
    def change_direction(self, action):
        
        """
            Change the direction of the snake
            that the class has stored. It does this
            based on an action which can be:
            a) action = 0: go left
            b) action = 1: go right
            c) action = 2: go straight
            The action is based on the snakes past direction
        """

        if self.direction==0: #left
            if action==0: #left
                self.direction=3
            elif action==1: #right
                self.direction=2
        elif self.direction==1: #right
            if action==0: #left
                self.direction=2
            elif action==1: #right
                self.direction=3
        elif self.direction==2: #up
            if action==0: #left
                self.direction=0
            elif action==1: #right
                self.direction=1
        elif self.direction==3: #down
            if action==0: #left
                self.direction=1
            elif action==1: #right
                self.direction=0


    def get_state(self):
        
        """
            Gets current state of the snake in the enviorment.
            Observations:
            A)Direction:
            0 - left
            1 - right
            2 - up
            3 - down
            B)X,Y axis:
            The y axis increases from the top to the bottom and
            the x axis increases from the left to the right.
            C)Symbol meanings:
            ws = wall straight if the observer were the snake
            wl = wall left if the observer were the snake
            wr = wall right if the observer were the snake
            fs = food straight if the observer were the snake
            fl = food left if the observer were the snake
            fr = food right if the observer were the snake            
        """

        fx = self.foodx - self.snake_Head[0] #food position x
        fy = self.foody - self.snake_Head[1] #food position y
        x1 = self.snake_Head[0]         #snake head position x
        y1 = self.snake_Head[1]         #snake head position y
        

        if self.direction==0: #left
            ws = True if x1==0 else False
            wr = True if y1==0 else False
            wl = True if self.dis_height==y1+10 else False
            fs = True if fx<0 else False
            fr = True if fy<0 else False
            fl = True if fy>0 else False

            for x in self.snake_List[:-1]: 
                if x[0]==self.snake_Head[0] and (self.snake_Head[1]-x[1]==10): #same x diff y=-1/wall on right
                    wr = True
                elif x[0]==self.snake_Head[0] and (x[1]-self.snake_Head[1]==10): #same x diff y=1/wall on left
                    wl = True
                elif (self.snake_Head[0]-x[0]==10) and self.snake_Head[1]==x[1]:  #same y diff x
                    ws = True
                    
        elif self.direction==1: #right
            ws = True if self.dis_width==x1+10 else False
            wl = True if y1==0 else False
            wr = True if self.dis_height==y1+10 else False 
            fs = True if fx>0 else False
            fr = True if fy>0 else False
            fl = True if fy<0 else False

            for x in self.snake_List[:-1]: 
                if x[0]==self.snake_Head[0] and (self.snake_Head[1]-x[1]==10): #same x diff y=1/wall on left
                    wl = True
                elif x[0]==self.snake_Head[0] and (x[1]-self.snake_Head[1]==10): #same x diff y=-1/wall on right
                    wr = True
                elif (x[0]-self.snake_Head[0]==10) and self.snake_Head[1]==x[1]:  #same y diff x
                    ws = True

        elif self.direction==2: #up
            wl = True if x1==0 else False
            wr = True if self.dis_width==x1+10 else False
            ws = True if y1==0 else False
            fs = True if fy<0 else False
            fr = True if fx>0 else False
            fl = True if fx<0 else False

            for x in self.snake_List[:-1]: 
                if  self.snake_Head[0]==x[0] and (self.snake_Head[1]-x[1]==10): #same x diff y
                    ws = True
                elif (x[0] - self.snake_Head[0]==10) and self.snake_Head[1]==x[1]: #same y diff x
                    wr = True
                elif (self.snake_Head[0]-x[0]==10) and self.snake_Head[1]==x[1]:  #same y diff x
                    wl = True

        else: #down
            wl = True if self.dis_width==x1+10 else False
            wr = True if x1==0 else False
            ws = True if self.dis_height==y1+10 else False
            fs = True if fy>0 else False
            fr = True if fx<0 else False
            fl = True if fx>0 else False

            for x in self.snake_List[:-1]: 
                if  self.snake_Head[0]==x[0] and (x[1]-self.snake_Head[1]==10): #same x diff y
                    ws = True
                elif (x[0] - self.snake_Head[0]==10) and self.snake_Head[1]==x[1]: #same y diff x
                    wl = True
                elif (0<self.snake_Head[0]-x[0]==10) and self.snake_Head[1]==x[1]:  #same y diff x
                    wr = True
        return_state=\
        [ws,wl,wr,fr,fl,fs,self.direction]
        
        return return_state

    def move_head(self, action):
        
        """
            Move the snake head. It will move the snake (head and body).
            It will also draw the new position on the screen.
        """

        if self.direction==0: #left
            if action==0: #left
                x1_change = 0
                y1_change = self.snake_block
                
            elif action==1: #right
                x1_change = 0
                y1_change = -self.snake_block
            
            else:
                x1_change = -self.snake_block
                y1_change = 0

        elif self.direction==1: #right
            if action==0: #left
                x1_change = 0
                y1_change = -self.snake_block

            elif action==1: #right
                x1_change = 0
                y1_change = self.snake_block
            
            else:
                x1_change = -self.snake_block
                y1_change = 0

        elif self.direction==2: #up
            
            if action==0: #left
                x1_change = -self.snake_block
                y1_change = 0

            elif action==1: #right
                x1_change = self.snake_block
                y1_change = 0
            else:
                x1_change = 0
                y1_change = -self.snake_block

        elif self.direction==3: #down
            if action==0: #left
                x1_change = self.snake_block
                y1_change = 0
            elif action==1: #right
                x1_change = -self.snake_block
                y1_change = 0
            else:
                x1_change = 0
                y1_change = self.snake_block

        #head direction change
        self.x1 += x1_change
        self.y1 += y1_change
        
        #draws new position
        self.dis.fill(self.blue)
        pygame.draw.rect(self.dis, self.green, [self.foodx, self.foody, self.snake_block, self.snake_block])
        
        #new snake position
        self.snake_Head = []
        self.snake_Head.append(self.x1)
        self.snake_Head.append(self.y1)
        self.snake_List.append(self.snake_Head)
        
        #if the snake is not only of size one, remove last position - 
        # since added an element, which is the head.
        if len(self.snake_List) > self.Length_of_snake:
            del self.snake_List[0]
        
        self.change_direction(action)

    ###########################
    #####GYM ENV FUNCTIONS#####
    ###########################

    def reset(self):
        pygame.QUIT
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption('Snake Game Reinforcment Learning')
        self.clock = pygame.time.Clock()
        
        self.snake_block = 10
        snake_speed = 25
        self.x1 = self.dis_width / 2
        self.y1 = self.dis_height / 2   
        self.snake_Head=[self.x1, self.y1] 
        self.snake_List = []
        self.Length_of_snake = 1
        self.foodx = round(random.randrange(0, self.dis_width-10) / 10.0) * 10.0
        self.foody = round(random.randrange(0, self.dis_height-10) / 10.0) * 10.0
        self.direction=0

        pygame.init()
        self.font_style = pygame.font.SysFont("comicsansms", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)
        return np.array(self.get_state())


    def step(self,action):
        
        """ 
            This function does the step of the game loop, and the game screen.
            It also handles the enviornment steps and agent updates. 
        """
        game_over=False
        old_dist=sqrt( (self.x1-self.foodx)**2 + (self.y1-self.foody)**2 )

        self.move_head(action)

        new_dist=sqrt( (self.x1-self.foodx)**2 + (self.y1-self.foody)**2 )

        if new_dist>=old_dist:
            reward_type=4
        else:
            reward_type=3
        
        for x in self.snake_List[:-1]:
            if x == self.snake_Head:
                game_over = True
                reward_type=2
                break

        if self.x1 >= self.dis_width or self.x1 < 0 or self.y1 >= self.dis_height or self.y1 < 0:
            game_over = True
            reward_type=2

        self.draw_snake(self.snake_block)
        self.update_score(self.Length_of_snake - 1)

        pygame.display.update()

        if self.x1 == self.foodx and self.y1 == self.foody:
            self.foodx = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
            self.foody = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
            self.Length_of_snake += 1
            reward_type=1

        
        new_state=self.get_state()
        self.clock.tick(self.snake_speed)

        reward=self.map_type_to_val(reward_type)

        return np.array(new_state), reward, game_over, {}