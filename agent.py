import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI
from model import Linear_QNet, QTrainer
from plotter import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
DANGER=5


class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):
        
        cell_r = (game.player.x+1,game.player.y)
        cell_d = (game.player.x,game.player.y-1)
        cell_l = (game.player.x-1,game.player.y)
        cell_u = (game.player.x,game.player.y+1)

        state = [

            # Danger in the next possible cells (maybe we can do the distance to the danger)
            game.get_cell_info(cell_r) == DANGER, # Danger to the right
            game.get_cell_info(cell_d) == DANGER, # Danger down
            game.get_cell_info(cell_l) == DANGER, # Danger to the left
            game.get_cell_info(cell_u) == DANGER, # Danger up

            
            # Carrot location 
            game.carrot.x > game.player.x,  # carrot right
            game.carrot.y > game.player.y  # carrot down
            game.carrot.x < game.player.x,  # carrot left
            game.carrot.y < game.player.y,  # carrot up


            # knife location 
            game.knife.x > game.player.x,  # knife right
            game.knife.y > game.player.y  # knife down
            game.knife.x < game.player.x,  # knife left
            game.knife.y < game.player.y,  # knife up


            #  location 
            game.cow.x > game.player.x,  # cow right
            game.cow.y > game.player.y  # cow down
            game.cow.x < game.player.x,  # cow left
            game.cow.y < game.player.y,  # cow up
            
            ]

        return np.array(state, dtype=int)

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

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, len(final_move)-1)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()