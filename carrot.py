import pygame

#-----------------------------------------------------------------------------------------------------------------------
# Définir une classe pour les carottes
class Carrot(pygame.sprite.Sprite):
    def __init__(self, x, y, CELL_SIZE):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load('Map/Designs_candy/Glace/Glace_Sol.png')
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

#-----------------------------------------------------------------------------------------------------------------------

    # Méthode pour faire réapparaître la carotte à une nouvelle position aléatoire
    def respawn(self, x, y):
        self.rect.topleft = (x, y)
        self.x = x
        self.y = y
        print(self.rect.topleft)

#-----------------------------------------------------------------------------------------------------------------------

    def draw(self, surface):
        surface.blit(self.image, self.rect)