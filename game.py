import pygame
import pytmx
import pyscroll
from player import Player

#-----------------------------------------------------------------------------------------------------------------------

class Game:
    """
    Creation of the Game class which is used to define the environment such as the character and the map itself.
    """

    def __init__(self):

        #Initialize the map of size 900pixels and 600pixels with title "Survivor Simulator"
        self.screen = pygame.display.set_mode((900, 600))
        pygame.display.set_caption("Survivor Simulator")
        tmx_data = pytmx.util_pygame.load_pygame('tiled/map_.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())


        # Initialize character and get its initial position
        player_position = tmx_data.get_object_by_name('Spawn_character')
        self.player = Player(player_position.x, player_position.y)
        map_layer.zoom = 2

        # Add obstacles to a list of obstacles
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == 'obstacle':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)
        self.group.add(self.player)

#-----------------------------------------------------------------------------------------------------------------------

    def handle_input(self):
        """
        Link keyboard actions to move the character with the corresponding functions
        :return: void
        """
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
        if pressed[pygame.K_DOWN]:
            self.player.move_down()
        if pressed[pygame.K_LEFT]:
            self.player.move_left()
        if pressed[pygame.K_RIGHT]:
            self.player.move_right()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

#-----------------------------------------------------------------------------------------------------------------------

    def collisions(self):

        # Necessary to update the position of the character in case of collision
        self.group.update()

        #if collision go back to old_position. collidelist() compare the self.player.feet rectangle and the self.walls one
        if self.player.feet.collidelist(self.walls) > -1:
            self.player.move_back()

#-----------------------------------------------------------------------------------------------------------------------
    
    def run(self):
        """
        While running loop to call all the functions until the user quit the game window.

        :return: void
        """
        clock = pygame.time.Clock()
        running = True

        while running:
            self.player.save_location()
            self.handle_input()

            # Camera centered on the character
            self.group.center(self.player.rect.center)

            self.collisions()
            self.player.update()

            # Display the different elements
            self.group.draw(self.screen)
            pygame.display.flip()

            # tick() used to control the number of time the code go through the while loop every seconds - 120 FPS
            clock.tick(120)
        pygame.quit()