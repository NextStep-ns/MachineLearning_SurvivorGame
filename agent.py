import torch
import random
import numpy as np
from collections import deque
from ai_game import AIGame
from model import Linear_QNet, QTrainer
from plotter import plot,hist
from collections import namedtuple
Point = namedtuple('Point', 'x, y')
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
DANGER=5


class Agent:

    def __init__(self):
        self.n_games = 0
        self.nb_actions=5
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.input_size=8
        self.hidden_size=256
        self.output_size=self.nb_actions
        self.model = Linear_QNet(self.input_size,self.hidden_size,self.output_size)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def load_model(self,file_path):
        self.model.load(file_path)

    def state_update(self):
        self.state = [
            # Danger
            self.game.is_collision(0), # Danger to the right
            self.game.is_collision(1), # Danger down
            self.game.is_collision(2), # Danger to the left
            self.game.is_collision(3), # Danger up

            # Carrots
            self.game.where_is_carrot(0),
            self.game.where_is_carrot(1),
            self.game.where_is_carrot(2),
            self.game.where_is_carrot(3),

        ]
        return self.state

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def next_action(self):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80-self.n_games
        self.final_move = [0]*self.nb_actions
        if random.randint(0,80) < self.epsilon and self.mode==1:
            move = random.randint(0, len(self.nb_actions)-1)
            self.final_move[move] = 1
        
        else:
            state0 = torch.tensor(self.state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            self.final_move[move] = 1
    
    def train_agent(self,game,mode=1):
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        record = 0
        self.game=game
        self.mode=mode
        while True:
            # state
            state_old=self.state_update()

            # next move
            self.next_action()
            
            # perform move and get new state
            reward, done, score = game.play_step(self.final_move,self.n_games)
            state_new=self.state_update()

            # train short memory
            self.train_short_memory(state_old, self.final_move, reward, state_new, done)
            # remember
            self.remember(state_old, self.final_move, reward, state_new, done)
            if done or game.frame_iteration>200*(game.n_carrots+1):
                # train long memory, plot result
                game.reset()
                self.n_games += 1
                self.train_long_memory()

                if score > record:
                    record = score
                    self.model.save(score=record)

                print('Game', self.n_games, 'Score', score, 'Record:', record)

                plot_scores.append(score)
                total_score += score
                mean_score = total_score / self.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)
                


    def play_agent(self,game,mode=1):
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        record = 0
        self.game=game
        self.mode=mode
        while True:
            # state
            state_old=self.state_update()

            # next move
            self.next_action()
            
            # perform move and get new state
            reward, done, score = game.play_step(self.final_move,self.n_games)
            state_new=self.state_update()

            # train short memory
            self.train_short_memory(state_old, self.final_move, reward, state_new, done)
            # remember
            self.remember(state_old, self.final_move, reward, state_new, done)
            if done or game.frame_iteration>200*(game.n_carrots+1):
                # train long memory, plot result
                game.reset()
                self.n_games += 1
                self.train_long_memory()

                if score > record:
                    record = score
                    self.model.save(score=record)

                print('Game', self.n_games, 'Score', score, 'Record:', record)



def train():
    agent = Agent()
    game = AIGame()
    mode=2
    if mode==0:
        pass
    elif mode==1:
        agent.train_agent(game)
    elif mode==2:
        agent.load_model("./model_best_scores/model_score167_2024-05-21_10-40-58.pth")
        agent.play_agent(game,mode)
    


if __name__ == '__main__':
    train()