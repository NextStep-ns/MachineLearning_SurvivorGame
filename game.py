import pygame
import pytmx
import pyscroll
import sys
import random
import time
from player import Player
from carrot import Carrot

#-----------------------------------------------------------------------------------------------------------------------

class Game:
    """
    Creation of the Game class which is used to define the environment such as the character and the map itself.
    """
    def __init__(self):

        # ======================================= MAP INITILISATION ======================================
        #Initialize the map of size 900pixels and 600pixels with title "Survivor Simulator"
        self.width = 900
        self.heigth = 600
        self.screen = pygame.display.set_mode((self.width, self.heigth))

        pygame.display.set_caption("Survivor Simulator")
        tmx_data = pytmx.util_pygame.load_pygame('tiled/Island_case/first_level_map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)

        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, (self.width, self.heigth))

        # ======================================= OBJECT INIT ======================================
        # Initialize character and get its initial position
        player_position = tmx_data.get_object_by_name('Spawn_character')
        self.player = Player(player_position.x, player_position.y)
        map_layer.zoom = 2

        # Add obstacles to a list of obstacles
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Add the player to the corresponding layer to be display on
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)
        self.group.add(self.player)

        #Initialize carrots
        self.carrot_group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)

        # ======================================= FLAGS ======================================
        self.interaction_carotte = False
        self.Carrots_exist = False

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

    def spawn_carrot(self, NbOfCarrots):
        if not self.Carrots_exist:
            for _ in range(NbOfCarrots):
                x = random.randint(0, self.width - 20)
                y = random.randint(0, self.heigth - 20)
                carrot = Carrot(x, y)

                self.carrot_group.add(carrot)
            self.carrot_group.update()

            print("carrots displayed")
            self.Carrots_exist = True

#-----------------------------------------------------------------------------------------------------------------------

    def update_carrots(self):
        self.carrot_group.update()
        if self.interaction_carotte:
            time.sleep(3)
            for carrot in self.carrot_group.sprites():
                carrot.respawn(self.width, self.heigth)
            self.interaction_carotte = False

#-----------------------------------------------------------------------------------------------------------------------

    def draw_carrots(self):
        # Dessinez chaque carotte dans le groupe de sprites sur la surface de jeu
        for carrot in self.carrot_group:
            self.group.add(carrot)

#-----------------------------------------------------------------------------------------------------------------------

    def game_over(self):
        """
        Function to display game over message and quit the game
        """
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()
        pygame.time.delay(3000)  # Pause for 3 seconds before quitting
        pygame.quit()
        sys.exit()

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

            #Display life bar
            self.player.lifebar(self.group, self.screen)
            pygame.display.flip()

            # Check if player's life is zero
            if self.player.life <= 0:
                self.game_over()

            # Camera centered on the character
            self.group.center(self.player.rect.center)

            self.collisions()
            self.player.update()

            # Display the different elements
            self.group.draw(self.screen)

            # Carrots
            self.spawn_carrot(5)
            self.update_carrots()
            self.draw_carrots()
            pygame.display.flip()

            # tick() used to control the number of time the code go through the while loop every seconds - 120 FPS
            clock.tick(120)
        pygame.quit()
