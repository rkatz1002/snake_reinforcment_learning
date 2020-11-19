from algorithms.sarsa import sarsa
from algorithms.monte_carlo import monte_carlo
import numpy as np

class RL():

    epsilon = 0.95
    Q={}
    reward_eat_food = 100
    reward_loose = - 500
    reward_do_nothing = - 10
    reward_do_nothing_go_further_away= - 50
    algorithm="SARSA"

    def __init__(self, algorithm):
        self.algorithm=algorithm
        if self.algorithm == "MONTE CARLO":
            self.returns={}
            for ws in [False,True]:
                self.returns[ws]={}
                for wl in [False,True]:
                    self.returns[ws][wl]={}
                    for wr in [False,True]:
                        self.returns[ws][wl][wr]={}
                        for direction in ['0', '1', '2', '3']:
                            self.returns[ws][wl][wr][direction]={}
                            for is_left in [False,True]:
                                self.returns[ws][wl][wr][direction][is_left]={}                        
                                for is_up in [False,True]:    
                                    self.returns[ws][wl][wr][direction][is_left][is_up]=[]
        
    def init_q(self, type="zeros"):        

        """
            This function starts the Q table of reinforcment learning.
            If the argument type=None, all elements will be zeros.
            If the kwarg type is ones, all elements of the Q table will
            be ones. 
        """

        if type=="ones":
            val=1
        elif type=="zeros":
            val=0

        for ws in [False,True]:
            self.Q[ws]={}
            for wl in [False,True]:
                self.Q[ws][wl]={}
                for wr in [False,True]:
                    self.Q[ws][wl][wr]={}
                    for direction in ['0', '1', '2', '3']:
                        self.Q[ws][wl][wr][direction]={}
                        for is_left in [False,True]:
                            self.Q[ws][wl][wr][direction][is_left]={}                        
                            for is_up in [False,True]:    
                                self.Q[ws][wl][wr][direction][is_left][is_up]=[val, val, val, val]
        

    def epsilon_greedy(self, s, train=False):
        
        def argmaxsecond(x):
            L = np.argsort(-np.array(x))
            top_n_2 = L[1]
            return top_n_2

        """
            policy epsilon greedy. Epsilon is defined in the class.
        """

        if train or np.random.rand() < self.epsilon:
            action = np.argmax(
                self.Q[s[0]][s[1]]\
                [s[2]][str(s[3])]\
                [True if s[4]<0 else False]\
                [True if s[5]<0 else False][:])
            #s[4] = foodx - x[0] => if is right, will be >0
            #s[5] = foody - x[1] => if is up, will be >0
        else:
            action = np.random.randint(0, 4)
        
    
        direction=int(s[3])

        #fix bugs to not go backwards
        if (direction==0 and action==1) or\
        (direction==1 and action==0) or\
        (direction==2 and action==3) or\
        (direction==3 and action==2):
            if train or np.random.rand() < self.epsilon:
                action = argmaxsecond(
                    self.Q[s[0]][s[1]]\
                    [s[2]][str(s[3])]\
                    [True if s[4]<0 else False]\
                    [True if s[5]<0 else False][:])
                    #s[4] = foodx - x[0] => if is right, will be >0
                    #s[5] = foody - x[1] => if is up, will be <0
            else:
                will_go_backwars=True
                while will_go_backwars:
                    action = np.random.randint(0, 4)
                    will_go_backwars=False
                    if (direction==0 and action==1) or\
                    (direction==1 and action==0) or\
                    (direction==2 and action==3) or\
                    (direction==3 and action==2):
                        will_go_backwars=True

        return action
    
    def write_q_table(self):

        """
            Will right the q table to txt file
            so user can run code whenever needed.
        """

        with open('rewards.txt', 'w') as file:
            for ws in self.Q:
                for wl in self.Q[ws]:
                    for wr in self.Q[ws][wl]:
                        for direction in self.Q[ws][wl][wr]:
                            for is_left in self.Q[ws][wl][wr][direction]:
                                for is_up in self.Q[ws][wl][wr][direction][is_left]:
                                    for reward in self.Q[ws][wl][wr][direction][is_left][is_up]:     
                                        file.write(str(reward)+';')
                                    file.write("\n")                                
            file.close()

    def read_q_table(self):
        
        """
            read q table from file
            so user can run code whenever needed.
        """
        
        with open('rewards.txt', 'r') as file:
            for ws in self.Q:
                for wl in self.Q[ws]:
                    for wr in self.Q[ws][wl]:
                        for direction in self.Q[ws][wl][wr]:
                            for is_left in self.Q[ws][wl][wr][direction]:
                                for is_up in self.Q[ws][wl][wr][direction][is_left]:
                                    line=file.readline()
                                    line=line.split(';')
                                    del line[-1]
                                    line=[float(numb) for numb in line]
                                    self.Q[ws][wl][wr][direction][is_left][is_up]=line
            file.close()

    def update_Q(self, state, action, new_state, new_action, reward_type):
        
        if self.algorithm=="SARSA":
        
            self.Q=sarsa(
                Q=self.Q,
                reward_eat_food=self.reward_eat_food,
                reward_loose=self.reward_loose,
                reward_do_nothing=self.reward_do_nothing,
                reward_do_nothing_go_further_away=self.reward_do_nothing_go_further_away,
                state=state,
                action=action,
                state_=new_state,
                action_=new_action,
                reward_type=reward_type,
                gamma=0.95,
                alpha=0.1
            )

        elif self.algorithm == "MONTE CARLO":
        
            self.G = 0
            
            self.Q=monte_carlo(
                Q=self.Q,
                reward_eat_food=self.reward_eat_food,
                reward_loose=self.reward_loose,
                reward_do_nothing=self.reward_do_nothing,
                reward_do_nothing_go_further_away=self.reward_do_nothing_go_further_away,
                state=state,
                action=action,
                state_=new_state,
                action_=new_action,
                reward_type=reward_type,
                gamma=0.95,
                returns=self.returns,
                G=self.G
            )