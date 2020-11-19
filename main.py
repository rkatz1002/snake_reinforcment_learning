import pygame
from enviorment import Snake_game
from tqdm import tqdm
from helper.plot import plot
from helper.write_scores import write_scores

def main():

    MAX_NUMBER_OF_STEPS=-1
    MAX_NUMBER_OF_EPISODES=10000
    n_episodes=0
    type_of_agent=-1
    scores=[]

    while type_of_agent not in [1,2,3]:
        print("What agent are we going to use?")
        print("1:                        Sarsa")
        print("2:                   Q Learning")
        print("3:              Deep Q Learning")

        type_of_agent = int(input())

    if type_of_agent==1:
        from agents.sarsa import Sarsa
        agent=Sarsa()
        file_name='Sarsa'
    elif type_of_agent==2: #TODO
        file_name='QLearning'
        pass 
        
    elif type_of_agent==3:
        from agents.deep_q_learning import DQN
        file_name='DeepQLearning'
        agent= DQN()
    
    for n_episodes in tqdm(range(MAX_NUMBER_OF_EPISODES)):
        
        game = Snake_game()

        n_steps=0
        game_over = False
        
        action=0
        action_=0
        state=game.get_state(action)
        
        while not game_over and n_steps!=MAX_NUMBER_OF_STEPS:

            n_steps+=1

            state_, game_over, reward_type = game.step(action_)

            action=action_
            action_ = agent.get_act(state_)

            agent.update(state, action, state_, action_, reward_type)

            state=state_

        scores.append(game.Length_of_snake)
        pygame.QUIT
        del game
    
    plot(scores)
    for score in scores:
        write_scores(file_name, score)


main()