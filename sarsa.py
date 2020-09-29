import numpy as np
from tqdm import tqdm
from state_to_game import StateActions

class SARSA():

    """
    Implements SARSA
    """

    alpha = 0.1
    gamma = 0.95
    epsilon = 0.95
    Q={}
    reward_eat_food = 500
    reward_loose = - 100
    reward_do_nothing = - 10
    reward_do_nothing_go_further_away= - 15

    def init_q(self, type="zeros"):        
        
        if type=="ones":
            val=1
        elif type=="zeros":
            val=0

        for ws in [False,True]:
            if ws not in self.Q:
                self.Q[ws]={}
            for wl in [False,True]:
                if wl not in self.Q[ws]:
                    self.Q[ws][wl]={}
                for wr in [False,True]:
                    if wr not in self.Q[ws][wl]:
                        self.Q[ws][wl][wr]={}
                    for is_left in [False,True]:
                        if is_left not in self.Q[ws][wl][wr]:
                            self.Q[ws][wl][wr][is_left]={}                        
                        for is_up in [False,True]:    
                            self.Q[ws][wl][wr][is_left][is_up]=[val, val, val, val]
        

    def epsilon_greedy(self, n_actions, s, last_event_type, train=False):
        
        """
        @param Q Q values state x action -> value
        @param epsilon for exploration
        @param s number of states
        @param train if true then no random actions selected
        """
        def argmaxsecond(x):
            L = np.argsort(-np.array(x))
            top_n_2 = L[1]
            return top_n_2

        if train or np.random.rand() < self.epsilon:
            action = np.argmax(
                self.Q[s[0]]\
                [s[1]][s[2]]\
                [True if s[3]<=0 else False]\
                [True if s[4]>=0 else False][:])
            #s[3] = foodx - x[0] => if is right, will be >0
            #s[4] = foody - x[1] => if is up, will be >0
        else:
            action = np.random.randint(0, n_actions)
        
        #fix bugs to not go backwards
        if (last_event_type==0 and action==1) or\
        (last_event_type==1 and action==0) or\
        (last_event_type==2 and action==3) or\
        (last_event_type==3 and action==2):
            if train==False:
                action = argmaxsecond(
                    self.Q[s[0]]\
                    [s[1]][s[2]]\
                    [True if s[3]<=0 else False]\
                    [True if s[4]>=0 else False][:])
                    #s[3] = foodx - x[0] => if is right, will be >0
                    #s[4] = foody - x[1] => if is up, will be >0
            else:
                will_go_backwars=True
                while will_go_backwars:
                    action = np.random.randint(0, n_actions)
                    will_go_backwars=False
                    if (last_event_type==0 and action==1) or\
                    (last_event_type==1 and action==0) or\
                    (last_event_type==2 and action==3) or\
                    (last_event_type==3 and action==2):
                        will_go_backwars=True
        return action
    
    def write_rewards_to_file(self):
        with open('rewards.txt', 'w') as file:
            for ws in self.Q:
                for wl in self.Q[ws]:
                    for wr in self.Q[ws][wl]:
                        for is_left in self.Q[ws][wl][wr]:
                            for is_up in self.Q[ws][wl][wr][is_left]:
                                for reward in self.Q[ws][wl][wr][is_left][is_up]:     
                                    file.write(str(reward)+';')
                                file.write("\n")                                
            file.close()

    def read_rewards_to_file(self):
        with open('rewards.txt', 'r') as file:
            for ws in self.Q:
                for wl in self.Q[ws]:
                    for wr in self.Q[ws][wl]:
                        for is_left in self.Q[ws][wl][wr]:
                            for is_up in self.Q[ws][wl][wr][is_left]:
                                line=file.readline()
                                line=line.split(';')
                                del line[-1]
                                line=[float(numb) for numb in line]
                                self.Q[ws][wl][wr][is_left][is_up]=line
            file.close()    
            
    def UpdateQ(self, state, action, state_, action_, reward_type):
        
        def map_type_to_val():
            if reward_type==1:
                return self.reward_eat_food
            
            elif reward_type==2:
                return self.reward_loose
                
            elif reward_type==3:
                return self.reward_do_nothing

            elif reward_type==4:
                return self.reward_do_nothing_go_further_away

        reward=map_type_to_val()

        q = self.Q[state[0]]\
                [state[1]][state[2]]\
                [True if state[3]<=0 else False]\
                [True if state[4]>=0 else False][action]
        
        
        q_=self.Q[state_[0]]\
        [state_[1]][state_[2]]\
        [True if state_[3]<=0 else False]\
        [True if state_[4]>=0 else False][action_]

        q += self.alpha * (reward + self.gamma * q_ - q)

        self.Q[state[0]]\
        [state[1]][state[2]]\
        [True if state[3]<=0 else False]\
        [True if state[4]>=0 else False][action] = q

