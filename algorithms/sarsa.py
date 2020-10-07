import numpy as np

def sarsa(
        Q, 
        reward_eat_food,
        reward_loose,
        reward_do_nothing,
        reward_do_nothing_go_further_away, 
        state, 
        action, 
        state_, 
        action_, 
        reward_type,
        gamma,
        alpha
    ):
        
    def map_type_to_val():
        if reward_type==1:
            return reward_eat_food
        
        elif reward_type==2:
            return reward_loose
            
        elif reward_type==3:
            return reward_do_nothing

        elif reward_type==4:
            return reward_do_nothing_go_further_away

    reward=map_type_to_val()

    q = Q[state[0]][state[1]]\
            [state[2]][str(state[3])]\
            [True if state[4]<0 else False]\
            [True if state[5]<0 else False]\
            [action]
    
    if state_ is not None:
        q_=Q[state_[0]][state_[1]]\
        [state_[2]][str(state_[3])]\
        [True if state_[4]<0 else False]\
        [True if state_[5]<0 else False]\
        [action_]
    else:
        q_=0

    q += alpha * (reward + gamma * q_ - q)

    Q[state[0]][state[1]]\
    [state[2]][str(state[3])]\
    [True if state[4]<0 else False]\
    [True if state[5]<0 else False]\
    [action] = q

    return Q