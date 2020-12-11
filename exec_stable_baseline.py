from enviorment import Snake_game
from stable_baselines import A2C, PPO1, PPO2, DQN
from tqdm import tqdm
from stable_baselines.bench.monitor import Monitor
def exec_stable_baseline(
        type_of_agent,
        train,
        TRAIN_MAX_NUMBER_OF_STEPS=17500,
        EVAL_MAX_NUMBER_OF_STEPS=2000,
        EVAL_MAX_NUMBER_OF_EPISODES=10,
        EVAL_NUMBER_OF_UPDATE_STEPS=1,
):

    # Define agent based on choosen type of agent
    
    env = Snake_game()
    
    if type_of_agent==3:
        file_name='DQN'
        if train:
            model = DQN(
                'MlpPolicy', 
                env,
                double_q=True
            ).learn(
                total_timesteps=TRAIN_MAX_NUMBER_OF_STEPS, 
                # reset_num_timesteps=False
            )
            model.save("stable_baseline_data\\dqn_snake")
        else:
            model = DQN(
                'MlpPolicy', 
                env
            ).load("stable_baseline_data\\dqn_snake")

    if type_of_agent==4:
        file_name='A2C'
        if train:
            model = A2C(
                'MlpPolicy', 
                env,
                gamma=0.99
            ).learn(
                total_timesteps=TRAIN_MAX_NUMBER_OF_STEPS, 
                reset_num_timesteps=False
            )
            model.save("stable_baseline_data\\a2c_snake")
        else:
            model = A2C(
                'MlpPolicy', 
                env
            ).load("stable_baseline_data\\a2c_snake")
    elif type_of_agent==5: 
        file_name='PPO1'
        if train:
            model = PPO1(
                'MlpPolicy', 
                env
            ).learn(
                total_timesteps=TRAIN_MAX_NUMBER_OF_STEPS, 
                reset_num_timesteps=False
            )
            model.save("stable_baseline_data\\pp01_snake")
        else:
            model = PPO1(
                'MlpPolicy', 
                env
            ).load("stable_baseline_data\\pp01_snake")
    elif type_of_agent==6: 
        file_name='PPO2'
        if train:
            model = PPO2(
                'MlpPolicy', 
                env
            ).learn(
                total_timesteps=TRAIN_MAX_NUMBER_OF_STEPS, 
                reset_num_timesteps=False
            )
            model.save("stable_baseline_data\\pp02_snake")
        else:
            model = PPO2(
                'MlpPolicy', 
                env
            ).load("stable_baseline_data\\pp02_snake")
    
    #start result arrays
    total_reward=0
    total_rewards=[]
    scores=[]

    #step and episode counter
    n_steps=1
    n_episodes=1
    done=False
    obs=env.reset()
    
    while n_episodes<EVAL_MAX_NUMBER_OF_EPISODES:
        n_episodes+=1
        n_steps=0
        while n_steps<EVAL_MAX_NUMBER_OF_STEPS:
            
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