import torch
import random
import numpy as np
from collections import deque
from game import GameAI
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
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(8, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):
        distance_r=0
        distance_d=0
        distance_l=0
        distance_u=0
        distance_c_r=0
        distance_c_d=0
        distance_c_l=0
        distance_c_u=0

        """
        for i in range(int(game.w-game.head.x)): #to the right
            cell_r = Point(game.head.x+1+i,game.head.y)
            if game.is_collision(cell_r):
                distance_r=i
                break
        for i in range(int(game.head.x)): # to the left
            cell_d = Point(game.head.x,game.head.y-1-i)
            if game.is_collision(cell_d):
                distance_r=i
                break
        for i in range(int(game.head.y)): # up
            cell_l = Point(game.head.x-1-i,game.head.y)
            if game.is_collision(cell_l):
                distance_r=i
                break
        for i in range(int(game.h-game.head.y)): # down
            cell_u = Point(game.head.x,game.head.y+1+i)
            if game.is_collision(cell_u):
                distance_r=i
                break
        if game.carrot.x - game.head.x:  # if >0 carrot is to the right
            distance_c_r=game.carrot.x - game.head.x
            distance_c_l=0
        else:
            distance_c_r=0
            distance_c_l=-(game.carrot.x - game.head.x)

        if game.carrot.y - game.head.y: # if >0 carrot is down
            distance_c_d=game.carrot.y - game.head.y
            distance_c_u=0
        else:
            distance_c_d=0
            distance_c_u=-(game.carrot.y - game.head.y)




        cell_r=Point(game.head.x+1,game.head.y)
        cell_d=Point(game.head.x,game.head.y+1)
        cell_l=Point(game.head.x-1,game.head.y)
        cell_u=Point(game.head.x,game.head.y-1)
            """

        
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
        self.epsilon = 120-self.n_games
        final_move = [0,0,0,0]
        if random.randint(0,120) < self.epsilon:
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
    plot_actions = [0,0,0,0]
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = GameAI()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)
        plot_actions[final_move.index(1)]+=1
        #hist(plot_actions)
        
        # perform move and get new state
        reward, done, score = game.play_step(final_move,agent.n_games)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        print(reward)
        # remember
        agent.remember(state_old, final_move, reward, state_new, done)
        if done or game.frame_iteration>200*(game.n_carrots+1):
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
            plot_actions = [0,0,0,0,0,0]


if __name__ == '__main__':
    train()