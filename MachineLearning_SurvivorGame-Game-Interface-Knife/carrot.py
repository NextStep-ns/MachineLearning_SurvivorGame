import pygame
import random
import time

#-----------------------------------------------------------------------------------------------------------------------

# Définir une classe pour les carottes
class Carrot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y
        self.image = pygame.image.load('tiled/2909789.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.Carrots_exist = False


#-----------------------------------------------------------------------------------------------------------------------

    # Méthode pour faire réapparaître la carotte à une nouvelle position aléatoire
    def respawn(self, width, height):
        while True:
            x = random.randint(0, len(self.sand_matrix)*16)
            y = random.randint(0, len(self.sand_matrix)*16)
            x_m,y_m=self.game_to_matrix_position(x, y)
            carrot_rect = pygame.Rect(x, y, 20, 20)
            if not (any(carrot_rect.colliderect(wall) for wall in self.walls)) and (self.sand_matrix[x_m][y_m]>=10):
                break
        self.rect.topleft = (x_m, y_m)

#-----------------------------------------------------------------------------------------------------------------------

    def draw(self, surface):
        surface.blit(self.image, self.rect)