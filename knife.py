import pygame

CELL_SIZE=128

class Knife(pygame.sprite.Sprite):
    def __init__(self, x, y, SIZE):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load('Map/Designs_candy/Marche massue/Massue.png')
        self.image = pygame.transform.scale(self.image, (SIZE, SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

#-----------------------------------------------------------------------------------------------------------------------

    # Méthode pour faire réapparaître la carotte à une nouvelle position aléatoire
    def respawn(self, x, y):
        self.rect.topleft = (x, y)
        self.x = x
        self.y = y
        print("Mass coordinate",self.rect.topleft)

#-----------------------------------------------------------------------------------------------------------------------

    def draw(self, surface):
        surface.blit(self.image, self.rect)