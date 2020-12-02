import numpy as np

class Sarsa():

    #q table
    Q={}
    
    #parameters
    alpha=0.1
    gamma=0.95
    epsilon = 0.95
    
    def __init__(self):
        self.init_q()

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
                    for fr in [False, True]:
                        self.Q[ws][wl][wr][fr]={}
                        for fl in [False, True]:
                            self.Q[ws][wl][wr][fr][fl]={}
                            for fs in [False, True]:
                                self.Q[ws][wl][wr][fr][fl][fs]={}
                                for direction in [0, 1, 2, 3]:
                                    self.Q[ws][wl][wr][fr][fl][fs][direction]=[val, val, val]
    def get_act(self, s, train=True):
        
        """
            policy epsilon greedy. Epsilon is defined in the class.
        """

        if train or np.random.rand() < self.epsilon:
            action = np.argmax(
                        self.Q\
                        [s[0]]\
                        [s[1]]\
                        [s[2]]\
                        [s[3]]\
                        [s[4]]\
                        [s[5]]\
                        [s[6]]
                    )
        else:
            action = np.random.randint(0, 3)
    
        return action
    
    def write_q_table(self):

        """
            Will right the q table to txt file
            so user can run code whenever needed.
        """

        with open('rewards.txt', 'w') as file:
            for ws in [False,True]:
                for wl in [False,True]:
                    for wr in [False,True]:
                        for fr in [False, True]:
                            for fl in [False, True]:
                                for fs in [False, True]:
                                    for direction in [0, 1, 2, 3]:
                                        for reward in self.Q[ws][wl][wr][fr][fl][fs][direction]:
                                            file.write(str(reward)+';')
                                        file.write("\n")                                
            file.close()

    def read_q_table(self):
        
        """
            read q table from file
            so user can run code whenever needed.
        """
        with open('rewards.txt', 'w') as file:
            for ws in self.Q:
                for wl in self.Q[ws]:
                    for wr in self.Q[ws][wl]:
                        for fr in self.Q[ws][wl][wr]:
                            for fl in self.Q[ws][wl][wr][fr]:
                                for fs in self.Q[ws][wl][wr][fr][fl]:
                                    for direction in self.Q[ws][wl][wr][fr][fl][fs]:
                                        line=file.readline()
                                        line=line.split(';')
                                        del line[-1]
                                        line=[float(numb) for numb in line]
                                        self.Q[ws][wl][wr][fr][fl][fs][direction]=line
                                        file.write("\n")                                
            file.close()

    def update(
            self, 
            state, 
            action, 
            state_, 
            action_, 
            reward
        ):

        def sarsa(
                Q,
                state, 
                action, 
                state_, 
                action_, 
                reward,
                gamma,
                alpha
            ):
        

            q = Q[state[0]][state[1]]\
                [state[2]][state[3]]\
                [state[4]][state[5]]\
                [state[6]][action]
            
            if state_ is not None:
                q_= Q[state_[0]][state_[1]]\
                    [state_[2]][state_[3]]\
                    [state_[4]][state_[5]]\
                    [state_[6]][action_]
            else:
                q_=0

            q += alpha*(reward + gamma*q_ - q)

            Q[state[0]][state[1]]\
            [state[2]][state[3]]\
            [state[4]][state[5]]\
            [state[6]][action] = q

            return Q

        self.Q=sarsa(
            Q=self.Q,
            state=state,
            action=action,
            state_=state_,
            action_=action_,
            reward=reward,
            gamma=self.gamma,
            alpha=self.alpha
        )
