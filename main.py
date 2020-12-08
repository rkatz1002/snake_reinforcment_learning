import pygame
from enviorment import Snake_game
from tqdm import tqdm
from helper.write_data import write_data
from exec_implementations import exec_implementations
# from exec_stable_baseline import exec_stable_baseline
import sys

def main():
    try:
        type_of_agent=int(sys.argv[-1])
    except:
        type_of_agent=-1

    while type_of_agent not in [1,2,3,4,5,6]:
        print("=============================================")
        print("What agent are we going to use?")
        print("1:                                      Sarsa")
        print("2:                                 Q Learning")
        print("3:                            Deep Q Learning")
        print("4:                Advantage Actor-Critic(A2C)")
        print("5:       Proximal Policy Optimization 1(PPO1)")
        print("6:       Proximal Policy Optimization 2(PPO2)")
        print("=============================================")

        type_of_agent = int(input())

    if type_of_agent in [1,2,3]:
        total_rewards, scores, file_name=exec_implementations(type_of_agent)
    
    elif type_of_agent in [4,5,6]:
        total_rewards, scores, file_name=exec_stable_baseline(type_of_agent)

    for total_reward in total_rewards:
        write_data(
            file_name+'_'+'total_rewards',
            total_reward
        )
    for score in scores:
        write_data(
            file_name+'_'+'score',
            score
        )


main()