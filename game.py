import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

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
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 40

class SnakeGameAI:

    def __init__(self, w=640, h=480):
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

        self.head = [Point(self.w/2, self.h/2)]
        self.score = 0
        self.carrot = None
        self._place_food()
        self.frame_iteration = 0


    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.carrot = Point(x, y)
        if self.carrot in self.head:
            self._place_food()


    def play_step(self, action):
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
        if self.is_collision() or self.frame_iteration > 10000*(self.score+1):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if action[-1] == 1 and self.head[0] == self.carrot:
            self.score += 1
            reward = 10
            self._place_food()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score


    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head[0]
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True

        return False


    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.head:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.carrot.x, self.carrot.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
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

        x = self.head[0].x
        y = self.head[0].y

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

        self.head[0] = Point(x, y)