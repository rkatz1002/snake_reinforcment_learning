import pygame
from enviorment import Snake_game
from tqdm import tqdm

def exec_implementations(
        type_of_agent,
        train,
        TRAIN_MAX_NUMBER_OF_STEPS=10000,
        EVAL_MAX_NUMBER_OF_STEPS=2000,
        EVAL_MAX_NUMBER_OF_EPISODES=10,
        EVAL_NUMBER_OF_UPDATE_STEPS=1,
    ):


    # Define agent based on choosen type of agent

    if type_of_agent==1:
        from agents.sarsa import Sarsa
        agent=Sarsa()
        file_name='Sarsa'

    elif type_of_agent==2: #TODO
        from agents.q_learning import QLearning
        agent=QLearning()
        file_name='QLearning'
        
    elif type_of_agent==3:
        from agents.deep_q_learning import DQN
        file_name='DeepQLearning'
        agent= DQN()
    
    #start some arrays
    n_steps=0
    total_reward=0
    total_rewards=[]
    scores=[]

    if not train:
        agent.read_q_table()
    
    elif train:
        env = Snake_game()
        n_steps=0
        game_over = False
        
        action=0
        action_=0
        state=env.get_state()

        while n_steps<TRAIN_MAX_NUMBER_OF_STEPS:
                
            n_steps+=1

            state_, reward, game_over, _ = env.step(action_)
            
            total_reward+=reward
            total_rewards.append(total_reward)

            action=action_
            action_ = agent.get_act(state_)

            if n_steps%EVAL_NUMBER_OF_UPDATE_STEPS==0:
                agent.update(state, action, state_, action_, reward)
                score=env.Length_of_snake-1
            
            state=state_
            
            if game_over:
                pygame.QUIT
                del env
                env = Snake_game()
                game_over = False
                
                action=0
                action_=0
                state=env.get_state()


        

    
        agent.write_q_table()

    for n_episodes in tqdm(range(1,EVAL_MAX_NUMBER_OF_EPISODES)):

        env = Snake_game()
        n_steps=0
        game_over = False
        
        action=0
        action_=0
        state=env.get_state()

        while not game_over and n_steps<EVAL_MAX_NUMBER_OF_STEPS:

            n_steps+=1

            state_, reward, game_over, _ = env.step(action_)
            
            total_reward+=reward
            total_rewards.append(total_reward)

            action=action_
            action_ = agent.get_act(state_)

            if game_over or n_steps%EVAL_NUMBER_OF_UPDATE_STEPS==0:
                agent.update(state, action, state_, action_, reward)
                score=env.Length_of_snake-1

            state=state_

        
        pygame.QUIT
        del env
        scores.append(score)
    
    if train:
        agent.write_q_table()
    
    return total_rewards, scores, file_name