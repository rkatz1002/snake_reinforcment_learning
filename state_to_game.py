import pygame

class StateActions():

    actions_events = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
    snake_length=0
    fx=0
    fy=0
    ws=False
    wr=False
    wl=False
    is_right=False
    is_up=False

    def __init__(self, foodx, foody, ws, wr, wl):
        self.fx=foodx
        self.fy=foody
        self.ws=ws
        self.wr=wr
        self.wl=wl
    
    def numb_to_event(self, numb):
        return self.actions_events[numb]
    def game_state_to_sarsa_state(self):
        if self.fx>=0:
            self.is_right=True
        if self.fy>=0:
            self.is_up=True
    def state_has_list(self):
        return [self.ws, self.wr , self.wl, self.is_right, self.is_up]