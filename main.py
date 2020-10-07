from reinforcment_learning import RL
from snake_game import Snake_game
import pygame
from matplotlib import pyplot as plt
from tqdm import tqdm

def main():

    number_of_episodes = 3000
    rl_object=RL("MONTE CARLO")
    rl_object.init_q()
    
    scores=[]
    episodes=[]
    
    rl_object.read_q_table()
    
    for i in tqdm(range(0,number_of_episodes)):

        file=open('scores.txt', 'a')
        
        game=Snake_game(rl_object=rl_object)
        score=game.gameLoop()  
        del game
        
        episodes.append(i+1)
        scores.append(score)
        file.write(str(score)+'\n')
        file.close()
        
        rl_object.write_q_table()
            
    plt.plot(episodes, scores)
    plt.show()


main()

