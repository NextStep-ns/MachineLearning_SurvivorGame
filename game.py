import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1000,200)

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

class ActionMouvement(Enum):
    STAY=0
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    INTERACT = 5

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
YELLOW = (200,200,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 200
SLOW_SPEED = 200

class SnakeGameAI:

    def __init__(self, w=680, h=680):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
        


    def reset(self):
        # init game state
        self.action_movement= ActionMouvement.STAY

        self.health=2000
        self.max_health=self.health
        self.score = 0
        self.carrot = None
        self.frame_iteration = 0
        self.wall=[
            Point(random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE, random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE),
            Point(random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE, random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE)
            ]
        self.head = Point(self.w/2,self.h/2)
        while self.is_collision(self.head):
            self.head = Point(random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE, random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE)
        self._place_food()


    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.carrot = Point(x, y)
        while self.is_collision(self.carrot):
            x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
            y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
            self.carrot = Point(x, y)
        
        if self.carrot.x == self.head.x and self.carrot.y == self.head.y:
            self._place_food()


    def play_step(self, action,n_games):
        self.health-=1
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 1000*(self.score+1) or self.health<=0:
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if action[-1] == 1 and self.head.x == self.carrot.x and self.head.y == self.carrot.y:
            self.score += 1
            self.health+=20
            reward = 10
            self._place_food()

        if action[0] == 1 :
            reward = -0.5
        
        # 5. update ui and clock
        self._update_ui(n_games)
        if n_games%50==0 and n_games !=0:
            self.clock.tick(SLOW_SPEED)
        else:
            self.clock.tick(SPEED)

        # 6. return game over and score
        return reward, game_over, self.score


    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        
        for block in self.wall:
            if (block.x <= pt.x < block.x + BLOCK_SIZE) and (block.y <= pt.y < block.y + BLOCK_SIZE):
                return True

        return False


    def _update_ui(self,n_games):
        self.display.fill(BLACK)

        pt=self.head
        pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
        for block in self.wall:
            pygame.draw.rect(self.display, YELLOW, pygame.Rect(block.x, block.y, BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.carrot.x, self.carrot.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        text = font.render("Game: " + str(n_games), True, WHITE)
        self.display.blit(text, [0, 25])
        text = font.render("Health: " + str(self.health), True, WHITE)
        self.display.blit(text, [0, 50])
        pygame.display.flip()


    def _move(self, action):

        clock_wise = [ActionMouvement.STAY,ActionMouvement.RIGHT, ActionMouvement.DOWN, ActionMouvement.LEFT, ActionMouvement.UP,ActionMouvement.INTERACT]
        if np.array_equal(action, [1, 0, 0, 0, 0, 0]):
            new_dir = clock_wise[0] # STAY

        if np.array_equal(action, [0, 1, 0, 0, 0, 0]):
            new_dir = clock_wise[1] # GO RIGHT
        
        if np.array_equal(action, [0, 0, 1, 0, 0, 0]):
            new_dir = clock_wise[2] # GO DOWN

        if np.array_equal(action, [0, 0, 0, 1, 0, 0]):
            new_dir = clock_wise[3] # GO LEFT

        if np.array_equal(action, [0, 0, 0, 0, 1, 0]):
            new_dir = clock_wise[4] # GO UP

        if np.array_equal(action, [0, 0, 0, 0, 0, 1]):
            new_dir = clock_wise[5] # INTERACT


        self.action_movement = new_dir

        x = self.head.x
        y = self.head.y

        if self.action_movement == ActionMouvement.STAY:
            pass
        elif self.action_movement == ActionMouvement.RIGHT:
            x += BLOCK_SIZE
        elif self.action_movement == ActionMouvement.LEFT:
            x -= BLOCK_SIZE
        elif self.action_movement == ActionMouvement.DOWN:
            y += BLOCK_SIZE
        elif self.action_movement == ActionMouvement.UP:
            y -= BLOCK_SIZE
        elif self.action_movement == ActionMouvement.INTERACT:
            pass

        self.head = Point(x, y)