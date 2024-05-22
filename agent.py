import torch
import random
import numpy as np
from collections import deque
from game import GameAI
from model import Linear_QNet, QTrainer
from plotter import plot
from collections import namedtuple

#-----------------------------------------------------------------------------------------------------------------------

Point = namedtuple('Point', 'x, y')

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
DANGER=5
TRESHOLD=1000
# MODEL=1 sans model, MODEL=2 avec model
MODEL = 1

#-----------------------------------------------------------------------------------------------------------------------

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.nb_actions = 5
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.input_size = 17
        self.hidden_size = 256
        self.output_size = self.nb_actions
        self.model = Linear_QNet(self.input_size, self.hidden_size, self.output_size)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    # -----------------------------------------------------------------------------------------------------------------------

    def load_model(self, file_path):
        self.model.load(file_path)

    # -----------------------------------------------------------------------------------------------------------------------

    def get_state(self, game):

        state = [
            # Danger
            game.is_collision(0), # Danger to the right
            game.is_collision(1), # Danger down
            game.is_collision(2), # Danger to the left
            game.is_collision(3), # Danger up

            # Carrots
            game.where_is_carrot(0),
            game.where_is_carrot(1),
            game.where_is_carrot(2),
            game.where_is_carrot(3),

            # Cows
            game.where_is_cow(0),
            game.where_is_cow(1),
            game.where_is_cow(2),
            game.where_is_cow(3),

            # Knife
            game.where_is_knife(0),
            game.where_is_knife(1),
            game.where_is_knife(2),
            game.where_is_knife(3),
            game.have_knife()
            ]
        
        print("STATE",state)
            
        return np.array(state, dtype=int)

    # -----------------------------------------------------------------------------------------------------------------------

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    # -----------------------------------------------------------------------------------------------------------------------

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    # -----------------------------------------------------------------------------------------------------------------------

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    # -----------------------------------------------------------------------------------------------------------------------

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = TRESHOLD-self.n_games
        final_move = [0,0,0,0,0]
        if random.randint(0,TRESHOLD) < self.epsilon:
            move = random.randint(0, len(final_move)-1)
            final_move[move] = 1
        
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

    # -----------------------------------------------------------------------------------------------------------------------

    def train_agent(self, game, mode=1):
        plot_scores = []
        plot_cow_scores = []
        plot_knife_scores = []
        plot_mean_scores = []
        total_score = 0
        record = 0
        self.game = game
        self.mode = mode
        while True:
            # state
            state_old = self.get_state(self.game)

            # next move
            self.final_move=self.get_action(state_old)

            # perform move and get new state
            reward, done, score, score_cow, score_knife = game.play_step(self.final_move, self.n_games)
            state_new = self.get_state(self.game)

            # train short memory
            self.train_short_memory(state_old, self.final_move, reward, state_new, done)
            # remember
            self.remember(state_old, self.final_move, reward, state_new, done)
            if done or game.frame_iteration > 200 * (game.n_carrots + 1):
                # train long memory, plot result
                game.reset()
                self.n_games += 1
                self.train_long_memory()

                if score > record:
                    record = score
                    self.model.save(score=record)

                print('Game', self.n_games, 'Score', score, 'Record:', record)

                plot_scores.append(score)
                plot_cow_scores.append(score_cow)
                plot_knife_scores.append(score_knife)
                total_score += score
                mean_score = total_score / self.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_cow_scores, plot_knife_scores)

    # -----------------------------------------------------------------------------------------------------------------------

    def play_agent(self, game, mode=1):
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        record = 0
        self.game = game
        self.mode = mode
        while True:
            # state
            state_old = self.get_state(self.game)

            # next move
            self.final_move = self.get_action(state_old)

            # perform move and get new state
            reward, done, score, score_cow, score_knife = game.play_step(self.final_move, self.n_games)
            state_new = self.get_state(self.game)

            # train short memory
            self.train_short_memory(state_old, self.final_move, reward, state_new, done)
            # remember
            self.remember(state_old, self.final_move, reward, state_new, done)
            if done or game.frame_iteration > 200 * (game.n_carrots + 1):
                # train long memory, plot result
                game.reset()
                self.n_games += 1
                self.train_long_memory()

                if score > record:
                    record = score
                    self.model.save(score=record)

                print('Game', self.n_games, 'Score', score, 'Record:', record)

#-----------------------------------------------------------------------------------------------------------------------

def train():
    agent = Agent()
    game = GameAI()
    if MODEL == 0:
        pass
    elif MODEL == 1:
        agent.train_agent(game)
    elif MODEL == 2:
        agent.load_model("/model_best_scores/model_2024-05-21_06-20-20.pth")
        agent.play_agent(game, MODEL)

#-----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    train()