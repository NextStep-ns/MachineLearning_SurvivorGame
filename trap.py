import pygame

SIZE_TRAP = 256
CELL_SIZE = 128
class Trap(pygame.sprite.Sprite):
    def __init__(self, x, y, SIZE):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load('Map/Designs_candy/Piège/Piège-1.png')
        self.image = pygame.transform.scale(self.image, (SIZE, SIZE))
        self.rect = pygame.Rect(x, y, SIZE, SIZE)
        self.rect.topleft = (self.x, self.y)

        # Load images for different directions
        self.images = {
            'trap': [pygame.image.load(
                f'Map/Designs_candy/Piège/Piège-{i}.png')
                     for i in range(1, 4)],
        }


#-----------------------------------------------------------------------------------------------------------------------

    # Méthode pour faire réapparaître la carotte à une nouvelle position aléatoire
    def respawn(self, x, y):
        self.rect.topleft = (x, y)
        print(self.rect.topleft)

#-----------------------------------------------------------------------------------------------------------------------

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def change_image(self, new_image_path):
        self.image = pygame.image.load(new_image_path)
        self.image = pygame.transform.scale(self.image, (SIZE_TRAP, SIZE_TRAP))