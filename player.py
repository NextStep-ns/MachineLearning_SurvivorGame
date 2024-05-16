import pygame

#-----------------------------------------------------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):

    def __init__(self,x ,y):
        super().__init__()
        self.x = x
        self.y = y
        self.sprite_sheet = pygame.image.load('tiled/aventurer_character(2).png')

        # Get a specific image of the spreadsheet
        self.image = self.get_image(364, 1065)

        # Transparency color set to black
        self.image.set_colorkey([0,0,0])

        # Create a rectangle around the character for collisions
        self.rect = self.image.get_rect()
        self.position = [self.x,self.y]
        print(self.position)

        self.speed = 3

        # Create a rectangle around the character's feet. Initialize at (0,0) that is topleft corner, the width and height
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.3, 12)

        # Keep in memory the old character position in case of collision
        self.old_position = self.position.copy()

        #HP of the player
        self.life=100
        self.max_health = 100

        # Initialize last update time
        self.last_update_time = pygame.time.get_ticks()

        # Initialize the inventory attribute as an empty list
        self.inventory = []

    #-----------------------------------------------------------------------------------------------------------------------

    def life_update(self):
        """
        Update player's life.
        """
        # Calculate elapsed time since last update
        now = pygame.time.get_ticks()
        elapsed_time = now - self.last_update_time

        # If 1 second has passed, decrease player's life by 1
        if elapsed_time >= 1000:
            self.life_evolution(-5)
            self.last_update_time = now

#-----------------------------------------------------------------------------------------------------------------------

    def life_evolution(self, change):
        """
        Method to increase or decrease player's life
        :param change: The amount by which the life should be changed
        :return: void
        """
        newlife = self.life + change
        if newlife > 100:
            self.life = 100
        elif newlife < 0:
            self.life = 0
        else:
            self.life = newlife

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

#-----------------------------------------------------------------------------------------------------------------------

    def add_to_inventory(self, item):
        self.inventory.append(item)

#-----------------------------------------------------------------------------------------------------------------------

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

#-----------------------------------------------------------------------------------------------------------------------

    def check_inventory(self, item):
        for object in self.inventory:
            if object == item:
                return True
        return False