# -*- coding: utf-8 -*-
"""
Created on Tue May 14 18:39:35 2024

@author: andre
"""

import os
import pygame
from game import Game
import subprocess

def select_game_mode():
    menu_font = pygame.font.Font(None, 36)
    text_play_human = menu_font.render("1. Play as a Human", True, (255, 255, 255))
    text_play_ai = menu_font.render("2. Play with AI", True, (255, 255, 255))

    screen.fill((0, 0, 0))
    screen.blit(text_play_human, (300, 200))
    screen.blit(text_play_ai, (300, 250))
    pygame.display.flip()

    mode = None
    while mode is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "human"
                elif event.key == pygame.K_2:
                    return "ai"

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("Survivor Simulator")

    while True:
        mode = select_game_mode()
        if mode is None:
            break
        elif mode == "human":
            subprocess.call(['python', 'main.py'])
        elif mode == "ai":
            subprocess.call(['python', 'play_ai.py']) # Il faudra bien entendu créer le fichier python

    pygame.quit()
