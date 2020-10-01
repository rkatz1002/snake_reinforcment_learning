from sarsa import SARSA
from snake_game import Snake_game
import pygame
from matplotlib import pyplot as plt
from tqdm import tqdm

def main():
    number_of_episodes = 3000
    sarsa=SARSA()
    sarsa.init_q()
    scores=[]
    episodes=[]
    sarsa.read_rewards_to_file()
    for i in tqdm(range(0,number_of_episodes)):
        file=open('scores.txt', 'a')
        game=Snake_game(sarsa=sarsa)
        score=game.gameLoop()  
        del game
        episodes.append(i+1)
        scores.append(score)
        file.write(str(score)+'\n')
        file.close()
        sarsa.write_rewards_to_file()
            
    plt.plot(episodes, scores)
    plt.show()


main()

