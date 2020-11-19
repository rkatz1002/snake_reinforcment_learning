
import random
import numpy as np
from keras import Sequential
from collections import deque
from keras.layers import Dense
import matplotlib.pyplot as plt
from keras.optimizers import Adam
import math

class DQN:

    """ Deep Q Network """
    
    #rewards
    reward_do_nothing_go_further_away=-2
    reward_loose=-100
    reward_do_nothing=1
    reward_eat_food=10
    
    #parameters
    action_space = 4 #number of actions
    state_space = 7  #number of states
    epsilon = 1
    gamma = 0.95
    batch_size = 500
    epsilon_min = 0.01
    epsilon_decay = 0.5 
    learning_rate = 0.00025
    layer_sizes = [128, 128, 128]

    def __init__(self):
        
        """
            Starts model and memory
        """
        
        self.memory = deque(maxlen=2500)
        self.model = self.build_model()


    def map_type_to_val(self, reward_type):
        
        """
            Map the type of reward to the value of the reward.
        """

        if reward_type==1:
            return self.reward_eat_food
        
        elif reward_type==2:
            return self.reward_loose
            
        elif reward_type==3:
            return self.reward_do_nothing

        elif reward_type==4:
            return self.reward_do_nothing_go_further_away

    def build_model(self):

        """
            Build the Neural Network model.
            For each layer use the relu function, thant the softmax function
            and optimize with MSE.
        """

        model = Sequential()
        for i in range(len(self.layer_sizes)):
            if i == 0:
                model.add(Dense(self.layer_sizes[i], input_shape=(self.state_space,), activation='relu'))
            else:
                model.add(Dense(self.layer_sizes[i], activation='relu'))
        model.add(Dense(self.action_space, activation='softmax'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model


    def remember(self, state, action, reward_type, next_state):
        """
            Store NN results.
        """
        reward=self.map_type_to_val(reward_type)
        
        np_state = np.reshape(np.array(state),(1,7))
        np_next_state = np.reshape(np.array(next_state),(1,7))

        self.memory.append((np_state, action, reward, np_next_state))


    def get_act(self, state):
        
        """
            Get best action from NN.
        """

        def argmaxsecond(x):
            L = np.argsort(-np.array(x))
            top_n_2 = L[1]
            return top_n_2
        
        np_state = np.reshape(np.array(state),(1,7))
        
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_space)
        act_values = self.model.predict(np_state)
        direction = np_state[-1][-1]

        action = np.argmax(act_values[0])
        action_2 = argmaxsecond(act_values[0])

        #Make sure snake doesnt go backwards

        if (direction==0 and action==1) or\
        (direction==1 and action==0) or\
        (direction==2 and action==3) or\
        (direction==3 and action==2):
            action=action_2
        
        return action


    def replay(self):
        
        """
            We can prevent action values from oscillating 
            or diverging catastrophically using a large buffer 
            of our past experience and sample training data from it,
            instead of using our latest experience. This technique is 
            called replay buffer or experience buffer. 
        """


        if len(self.memory) < self.batch_size:
            return

        minibatch = random.sample(self.memory, self.batch_size)
        states = np.array([i[0] for i in minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        targets = rewards + self.gamma*(np.amax(self.model.predict_on_batch(next_states), axis=1))
        targets_full = self.model.predict_on_batch(states)

        ind = np.array([i for i in range(self.batch_size)])
        targets_full[[ind], [actions]] = targets

        self.model.fit(states, targets_full, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update(self,state,action,state_,action_,reward_type):
        self.remember(state,action,reward_type,state_)
        self.replay()