import pygame

#-----------------------------------------------------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):

    def __init__(self,x ,y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('tiled/aventurer_character(2).png')

        # Get a specific image of the spreadsheet
        self.image = self.get_image(364, 1065)

        # Transparency color set to black
        self.image.set_colorkey([0,0,0])

        # Create a rectangle around the character for collisions
        self.rect = self.image.get_rect()
        self.position = [x,y]
        print(self.position)

        self.speed = 2

        # Create a rectangle around the character's feet. Initialize at (0,0) that is topleft corner, the width and height
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.3, 12)

        # Keep in memory the old character position in case of collision
        self.old_position = self.position.copy()

#-----------------------------------------------------------------------------------------------------------------------

    def save_location(self):
        """
        Keep in memory the old character position in case of collision
        :return: void
        """
        self.old_position = self.position.copy()

#-----------------------------------------------------------------------------------------------------------------------

    def move_right(self):
        self.position[0] += self.speed
    def move_left(self):
        self.position[0] -= self.speed
    def move_up(self):
        self.position[1] -= self.speed
    def move_down(self):
        self.position[1] += self.speed

#-----------------------------------------------------------------------------------------------------------------------

    def update(self):

        # Topleft corner of the rectange that surrounds the character
        self.rect.topleft = self.position

        #Bottom middle of the feet rectangle to match the position of the rect
        self.feet.midbottom = self.rect.midbottom

#-----------------------------------------------------------------------------------------------------------------------

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

#-----------------------------------------------------------------------------------------------------------------------

    def get_image(self, x, y):
        """
        Get a specific image of a spreadsheet in fucntion of the givens x and y
        :param x: x position of the desired image
        :param y: y position of the desired image
        :return: desired image
        """
        image = pygame.Surface([30,40])
        image.blit(self.sprite_sheet, (0,0), (x,y,30,40))
        return image