import pygame

class Cow(pygame.sprite.Sprite):
    def __init__(self, x, y, SIZE):
        super().__init__()
        self.SIZE = SIZE
        self.x = x
        self.y = y
        self.image = pygame.image.load('Map/Designs_candy/Vache/Vache-1.png')
        self.image = pygame.transform.scale(self.image, (SIZE, SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.cow_flag=0
        
        self.frames = [pygame.image.load(f'Map/Designs_candy/Vache/Vache-{i}.png') for i in range(1, 4)]
        self.current_frame = 0

        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 500  # Delay in milliseconds (500ms = 0.5s)

    def update_image(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay and self.cow_flag==0:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.image = pygame.transform.scale(self.image, (self.SIZE, self.SIZE))
#-----------------------------------------------------------------------------------------------------------------------

    # Méthode pour faire réapparaître la carotte à une nouvelle position aléatoire
    def respawn(self, x, y):
        self.rect.topleft = (x, y)
        self.x = x
        self.y = y
        self.image = pygame.image.load(f'Map/Designs_candy/Vache/Vache-{1}.png')
        self.image = pygame.transform.scale(self.image, (self.SIZE, self.SIZE))
        print("Cow coordinate",self.rect.topleft)

#-----------------------------------------------------------------------------------------------------------------------

    def draw(self, surface):
        surface.blit(self.image, self.rect)