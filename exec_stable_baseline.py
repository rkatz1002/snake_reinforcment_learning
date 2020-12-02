from enviorment import Snake_game
from stable_baselines import A2C, PPO1, PPO2
from tqdm import tqdm

def exec_stable_baseline(
        type_of_agent,
        MAX_NUMBER_OF_STEPS=10000,
        MAX_NUMBER_OF_EPISODES=10,
        NUMBER_OF_UPDATE_STEPS=10
):

    # Define agent based on choosen type of agent

    if type_of_agent==4:
        file_name='A2C'
        env = Snake_game()
        model = A2C(
            'MlpPolicy', 
            env,
            ent_coef=0
        ).learn(total_timesteps=MAX_NUMBER_OF_STEPS)
        model.save("stable_baseline_data\\a2c_snake")
    elif type_of_agent==5: 
        file_name='PPO1'
        env = Snake_game()
        model = PPO1(
            'MlpPolicy', 
            env
        ).learn(total_timesteps=MAX_NUMBER_OF_STEPS)
        model.save("stable_baseline_data\\pp01_snake")
    elif type_of_agent==6: 
        file_name='PPO2'
        env = Snake_game()
        model = PPO2(
            'MlpPolicy', 
            env
        ).learn(total_timesteps=MAX_NUMBER_OF_STEPS)
        model.save("stable_baseline_data\\pp02_snake")

    
    #start result arrays
    total_reward=0
    total_rewards=[]
    scores=[]

    #step and episode counter
    n_steps=1
    n_episodes=1
    done=False
    obs=env.reset()

    while n_episodes<MAX_NUMBER_OF_EPISODES:
        n_episodes+=1
        n_steps=0
        while n_steps<MAX_NUMBER_OF_STEPS:
            
            #update step counter
            n_steps+=1
            
            # if game done, reset enviorment
            if done:
                #update score results
                score=env.Length_of_snake-1
                scores.append(score)
                obs=env.reset()
            
            #do action
            action_, state = model.predict(obs)
            obs, reward, done, info = env.step(action_)
            
           
            
            #update reward results            
            total_reward+=reward
            total_rewards.append(total_reward)
            

    return total_rewards, scores, file_name    