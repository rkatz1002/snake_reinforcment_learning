import pygame
import time
import random
from sarsa import SARSA
from math import sqrt
import sys
import pdb

#https://www.edureka.co/blog/snake-game-with-pygame/

class Snake_game():
    white = (255, 255, 255)
    yellow = (255, 255, 102)
    black = (0, 0, 0)
    red = (213, 50, 80)
    green = (0, 255, 0)
    blue = (50, 153, 213)
    
    dis_width = 600
    dis_height = 400
    
    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('Snake Game Reinforcment Learning')
    
    clock = pygame.time.Clock()
    
    snake_block = 10
    snake_speed = 25
    sarsa=None
    pygame.init()
    
    font_style = pygame.font.SysFont("comicsansms", 25)
    score_font = pygame.font.SysFont("comicsansms", 35)
    
    def __init__(self,sarsa):
        self.sarsa=sarsa

    def Your_score(self, score):
        value = self.score_font.render("Your Score: " + str(score), True, self.yellow)
        self.dis.blit(value, [0, 0])

    def our_snake(self, snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.dis, self.black, [x[0], x[1], snake_block, snake_block])
    
    def get_state(self, snake_Head, foodx, foody, last_event_type, snake_List):
        
        fx = foodx - snake_Head[0]
        fy = foody - snake_Head[1]
        x1 = snake_Head[0]
        y1 = snake_Head[1]
        
        if last_event_type==0: #left
            ws = True if x1==0 else False
            wl = True if y1==0 else False
            wr = True if self.dis_height==y1 else False
            
            for x in snake_List: 
                if x[0]==snake_Head[0] and x[1]-snake_Head[1]==1: #same x diff y=-1/wall on right
                    wr = True
                elif x[0]==snake_Head[0] and snake_Head[1]-x[1]==1: #same x diff y=1/wall on left
                    wl = True
                elif  snake_Head[0]-x[0]==1 and snake_Head[1]==x[1]:  #same y diff x
                    ws = True

        elif last_event_type==1: #right
            ws = True if self.dis_width-x1==0 else False
            wr = True if y1==0 else False
            wl = True if self.dis_height-y1==0 else False 

            for x in snake_List: 
                if x[0]==snake_Head[0] and x[1]-snake_Head[1]==1: #same x diff y=1/wall on left
                    wl = True
                elif x[0]==snake_Head[0] and snake_Head[1]-x[1]==1: #same x diff y=-1/wall on right
                    wr = True
                elif x[0]-snake_Head[0]==1 and snake_Head[1]==x[1]:  #same y diff x
                    ws = True

        elif last_event_type==2: #up
            wl = True if x1==0 else False
            wr = True if self.dis_width-x1==0 else False
            ws = True if self.dis_height-y1==0 else False

            for x in snake_List: 
                if  snake_Head[0]==x[0] and x[1]-snake_Head[1]==1: #same x diff y
                    ws = True
                elif x[0] - snake_Head[0]==1 and snake_Head[1]==x[1]: #same y diff x
                    wr = True
                elif snake_Head[0]-x[0]==1 and snake_Head[1]==x[1]:  #same y diff x
                    wl = True

        else: #down
            wl = True if x1 == 0 else False
            wr = True if self.dis_width - x1 == 0 else False
            ws = True if y1 == 0 else False

            for x in snake_List: 
                if  snake_Head[0]==x[0] and snake_Head[1]-x[1]==1: #same x diff y
                    ws = True
                elif x[0] - snake_Head[0]==1 and snake_Head[1]==x[1]: #same y diff x
                    wl = True
                elif snake_Head[0]-x[0]==1 and snake_Head[1]==x[1]:  #same y diff x
                    wr = True      
        

        return [ws,wl,wr,fx,fy]

    def message(self, msg, color):
        mesg = self.font_style.render(msg, True, color)
        self.dis.blit(mesg, [self.dis_width / 6, self.dis_height / 3])
    
    def step(self, x1, y1, x1_change, y1_change, snake_List,Length_of_snake,foodx,foody,last_event_type):
        
        state=self.get_state([x1,y1], foodx, foody, last_event_type, snake_List)
        
        event_type=self.sarsa.epsilon_greedy(4, state, last_event_type)
        
        if event_type == 0: #left
            x1_change = -self.snake_block
            y1_change = 0
        elif event_type == 1: #right
            x1_change = self.snake_block
            y1_change = 0
        elif event_type == 2: #up
            y1_change = self.snake_block
            x1_change = 0
        elif event_type == 3: #down
            y1_change = -self.snake_block
            x1_change = 0

        x1 += x1_change
        y1 += y1_change
        self.dis.fill(self.blue)
        pygame.draw.rect(self.dis, self.green, [foodx, foody, self.snake_block, self.snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        new_state=self.get_state([x1,y1], foodx, foody, last_event_type, snake_List)

        return x1,y1,x1_change,\
        y1_change,snake_List,Length_of_snake,\
        foodx,foody, snake_Head, event_type, state, new_state
    
    def gameLoop(self):
        
        game_over = False
        game_close = False
    
        x1 = self.dis_width / 2
        y1 = self.dis_height / 2
    
        x1_change = 0
        y1_change = 0

        last_event_type=2
        
        snake_List = []
        Length_of_snake = 1
    
        foodx = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
    
        while not game_over:
    
            while game_close == True:
                self.dis.fill(self.blue)
                self.message("You Lost! Press C-Play Again or Q-Quit", self.red)
                self.Your_score(Length_of_snake - 1)
                pygame.display.update()
    
                game_over = True
                game_close = False

            old_dist=sqrt( (x1-foodx)**2 + (y1-foody)**2 )
            
            x1,y1,x1_change,\
            y1_change,snake_List,Length_of_snake,\
            foodx,foody, snake_Head, new_event_type,\
            old_state, new_state=\
            self.step(x1,y1,x1_change,y1_change,\
            snake_List,Length_of_snake,foodx,foody, last_event_type)

            new_dist=sqrt( (x1-foodx)**2 + (y1-foody)**2 )
            
            if new_dist>=old_dist:
                reward_type=4
            else:
                reward_type=3
            
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True
                    reward_type=2

            if x1 > self.dis_width or x1 < 0 or y1 > self.dis_height or y1 < 0:
                game_close = True
                reward_type=2

            self.our_snake(self.snake_block, snake_List)
            self.Your_score(Length_of_snake - 1)

            pygame.display.update()
    
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
                Length_of_snake += 1
                reward_type=1

            self.sarsa.UpdateQ(old_state, last_event_type, new_state, new_event_type, reward_type)
            last_event_type=new_event_type
            old_state=new_state
            self.clock.tick(self.snake_speed)
        
        pygame.QUIT
        return Length_of_snake - 1
# s = Snake_game()
# s.gameLoop()