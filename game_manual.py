import pygame
import pytmx
import pyscroll
import sys
import random
from player_manual import Player
#from firecamp import Firecamp
from carrot import Carrot
from cow import Cow
from knife import Knife
from trap import Trap

CELL_SIZE=128
ZOOM=0.5
SIZE_COW = 500
SIZE_CARROT = 128
SIZE_KNIFE = 256
SIZE_TRAP = 256
SIZE_PLAYER = 350

BONUS_CARROT=25
BONUS_COW=100
BONUS_KNIFE=0

#-----------------------------------------------------------------------------------------------------------------------

class Game:
    """
    Creation of the Game class which is used to define the environment such as the character and the map itself.
    """
    def __init__(self):
        # ======================================= MAP INITILISATION ======================================
        #Initialize the map of size 900pixels and 600pixels with title "Survivor Simulator"
        self.screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.FULLSCREEN)
        pygame.display.set_caption("Survivor Simulator")
        self.tmx_data = pytmx.util_pygame.load_pygame('Map/Tiled_map/Final_version_map.tmx')
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, (pygame.display.Info().current_w, pygame.display.Info().current_h))

        # Initialize UI elements
        self.initialize_lifebar()

        # ======================================= OBJECT INIT ======================================
        # Initialize character and get its initial position
        player_position = self.tmx_data.get_object_by_name('Spawn_character')
        self.player = Player(player_position.x, player_position.y, SIZE_PLAYER)
        self.map_layer.zoom = ZOOM

        # Add obstacles to a list of obstacles
        self.walls = []

        for obj in self.tmx_data.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Add obstacles to a list of obstacles
        self.water = []

        for obj in self.tmx_data.objects:
            if obj.type == 'water':
                self.water.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Add the player to the corresponding layer to be display on
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=3)
        self.group.add(self.player)

        self.start_ticks = pygame.time.get_ticks()
        #Initialize carrots
        self.carrot_group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=3)
        self.carrot_legend = Carrot(5, 30, 40)
        self.n_carrots = 0
        # Initialize cows
        self.cow_group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=2)
        self.cow_legend = Cow(2, 60, 40)

        self.n_cows = 0
        # Initialize knife
        self.knife_group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=3)
        self.knife_legend = Knife(5, 80, 40)
        self.n_knife = 0
        # Initialize trap
        self.trap_group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=2)
        # Initialize knife
        #self.firecamp_group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=3)
        #self.firecamp = Firecamp(319, 223)

        # Detect sand layer
        self.sand_matrix = self.tmx_data.get_layer_by_name("sand").data
        print(self.sand_matrix)

        # ======================================= FLAGS ======================================
        self.interaction_carrot = False
        self.interaction_cow = False
        self.interaction_knife = False
        self.interaction_trap = False
        self.interaction_water = False
        #self.interaction_firecamp = False
        #self.Firecamps_exist = False
        self.Traps_exist = False
        self.Carrots_exist = False
        self.Cows_exist = False
        self.Knifes_exist = False
        self.flagcarrot=0

#-----------------------------------------------------------------------------------------------------------------------

    def initialize_lifebar(self):
        """
        Initialize the life bar and heart image.
        """
        # Initialize the life bar
        self.lifebar_width = 200
        self.lifebar_height = 20
        self.lifebar_outer_rect = pygame.Rect(10, 10, self.lifebar_width, self.lifebar_height)
        self.lifebar_inner_rect = pygame.Rect(self.lifebar_outer_rect.left, self.lifebar_outer_rect.top + 2, 0,
                                              self.lifebar_height - 4)
        self.lifebar_color = (255, 0, 0)  # Red color

        # Load heart image
        self.heart_image = pygame.image.load('tiled/heart_lifebar.png')
        self.heart_height = self.lifebar_height + 10
        self.heart_image = pygame.transform.scale(self.heart_image, (self.heart_height, self.heart_height))
        self.heart_rect = self.heart_image.get_rect()
        self.heart_rect.topleft = (self.lifebar_outer_rect.left - 10, self.lifebar_outer_rect.top - 6)

        # Initialize the font
        self.font = pygame.font.Font(None, 36)

    # -----------------------------------------------------------------------------------------------------------------------

    def draw_elmt_minimap(self, obj, path):
        player_color = (0, 0, 0)

        if obj == self.player:
            obj_minimap_x = int(obj.rect.centerx / CELL_SIZE * self.block_size)
            obj_minimap_y = int(obj.rect.centery / CELL_SIZE * self.block_size)
            pygame.draw.circle(self.minimap_image, player_color, (obj_minimap_x, obj_minimap_y), 4)
        else:
            obj_minimap_x = int(obj.rect.centerx / CELL_SIZE * self.block_size)
            obj_minimap_y = int(obj.rect.centery / CELL_SIZE * self.block_size)

            self.elmt_minimap = pygame.image.load(path)
            self.elmt_minimap = pygame.transform.scale(self.elmt_minimap, (30, 30))
            self.minimap_image.blit(self.elmt_minimap, (obj_minimap_x - 15, obj_minimap_y - 15))

    # -----------------------------------------------------------------------------------------------------------------------

    def draw_minimap(self):

        """
        Draws a simple mini-map on the screen showing the player's current position.
        """
        self.minimap_size = 200  # The size of the mini-map
        self.block_size = self.minimap_size // 50  # Size of each block in the mini-map
        # self.minimap_surface = pygame.Surface((self.minimap_size, self.minimap_size))
        self.minimap_x = self.screen.get_width() - self.minimap_size - 20
        self.minimap_y = 20  # 20 pixels from the top

        self.minimap_image = pygame.image.load('tiled/minimap.JPG')
        self.minimap_image = pygame.transform.scale(self.minimap_image, (self.minimap_size, self.minimap_size))
        self.cadre_minimap_image = pygame.image.load('tiled/cadre_minimap.png')
        self.cadre_minimap_image = pygame.transform.scale(self.cadre_minimap_image, (317, 269))

        self.draw_elmt_minimap(self.player, "")
        for carrot in self.carrot_group:
            self.draw_elmt_minimap(carrot, 'Map/Designs_candy/Glace/Glace_Sol.png')

        for cow in self.cow_group:
            self.draw_elmt_minimap(cow, 'tiled/cow_minimap-removebg-preview.png')

        for knife in self.knife_group:
            self.draw_elmt_minimap(knife, 'Map/Designs_candy/Marche massue/Massue.png')

        self.screen.blit(self.minimap_image, (self.minimap_x - 10, self.minimap_y + 10))
        self.screen.blit(self.cadre_minimap_image, (self.minimap_x - 70, self.minimap_y - 25))

# -----------------------------------------------------------------------------------------------------------------------

    def have_knife(self):
        return "knife" in self.player.inventory

#-----------------------------------------------------------------------------------------------------------------------

    def game_to_matrix_position(self, x, y):
        """
        Convert game coordinates (x, y) to matrix indices (i, j).
        """
        taille_case = CELL_SIZE # Taille d'une case de la matrice
        i = (x // taille_case)
        j = (y // taille_case)
        return i, j

#-----------------------------------------------------------------------------------------------------------------------

    def update_screen(self):
        """
        Update the game screen.
        """
        # Camera centered on the character
        self.group.center(self.player.rect.center)

        # Draw the map and player
        self.group.draw(self.screen)

        # Update life bar
        life_percentage = self.player.life / self.player.max_health
        self.lifebar_inner_rect.width = int(self.lifebar_width * life_percentage - 2)
        self.lifebar_inner_rect.left = self.lifebar_outer_rect.left + 2

        # Draw outer life bar
        pygame.draw.rect(self.screen, (0, 0, 0), self.lifebar_outer_rect, 2)

        # Draw inner life bar
        pygame.draw.rect(self.screen, self.lifebar_color, self.lifebar_inner_rect)

        # Draw heart image
        self.screen.blit(self.heart_image, self.heart_rect)

        # Draw "Eat or Die" text
        text_surface = self.font.render("Eat or Die", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.lifebar_outer_rect.centerx, self.lifebar_outer_rect.centery))
        self.screen.blit(text_surface, text_rect)

        # Display time
        self.current_time = (pygame.time.get_ticks() - self.start_ticks) // 1000  # Convert milliseconds to seconds
        time_text = self.font.render(f": {self.current_time}", True, (0, 0, 0))
        self.screen.blit(time_text, (30, 125))  # Display at (0, 50) on the screen
        chrono_image = pygame.image.load('tiled/chrono.png')
        chrono_image = pygame.transform.scale(chrono_image, (35, 19))
        self.screen.blit(chrono_image, (0, 130))

        # Display carrots
        carrot_text = self.font.render(f": {self.n_carrots}", True, (0, 0, 0))
        self.screen.blit(carrot_text, (40, 50))  # Display at (0, 50) on the screen
        self.carrot_legend.draw(self.screen)

        # Display cows
        cow_text = self.font.render(f": {self.n_cows}", True, (0, 0, 0))
        self.screen.blit(cow_text, (40, 75))  # Display at (0, 50) on the screen
        self.cow_legend.draw(self.screen)

        # Display knifes
        knife_text = self.font.render(f": {self.n_knife}", True, (0, 0, 0))
        self.screen.blit(knife_text, (40, 100))  # Display at (0, 50) on the screen
        self.knife_legend.draw(self.screen)

        self.display_inventory()
        self.draw_minimap()

        for item in self.cow_group:
            item.update_image()

        # Update the display
        pygame.display.flip()

        # -----------------------------------------------------------------------------------------------------------------------
    def display_inventory(self):
        # Display inventory
        backpack_image = pygame.image.load('tiled/backpack.png')
        backpack_image = pygame.transform.scale(backpack_image, (50, 50))
        self.screen.blit(backpack_image, (5, 550))

        inventory_rect = pygame.Rect(54, 558, 35, 35)
        self.screen.fill((210, 180, 135), inventory_rect)

        cadre_image = pygame.image.load('tiled/cadre.png')
        cadre_image = pygame.transform.scale(cadre_image, (50, 50))
        self.screen.blit(cadre_image, (46, 550))

        if "knife" in self.player.inventory:
            self.knife_ = Knife(58, 560, 50)
            self.knife_.draw(self.screen)
        elif "knife" not in self.player.inventory:
            inventory_rect = pygame.Rect(54, 558, 35, 35)
            self.screen.fill((210, 180, 140), inventory_rect)
            self.screen.blit(cadre_image, (46, 550))
    
#-----------------------------------------------------------------------------------------------------------------------

    def handle_input(self):
        """
        Link keyboard actions to move the character with the corresponding functions
        :return: void
        """

        if self.pressed[pygame.K_UP]:
            self.player.move_up()
        elif self.pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif self.pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif self.pressed[pygame.K_RIGHT]:
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

    def collisions_water(self):

        # Necessary to update the position of the character in case of collision
        self.group.update()

        # if collision go back to old_position. collidelist() compare the self.player.feet rectangle and the self.walls one
        if self.player.feet.collidelist(self.water) > -1:
            self.player.life -= 0.5
            self.interaction_water = True

        else:
            if self.interaction_water:
                self.interaction_water = False


#-----------------------------------------------------------------------------------------------------------------------

    def spawn_item(self, Nbr, item):
        exist_attr = f"{item.capitalize()}s_exist"
        print(exist_attr)
        group = getattr(self, f"{item}_group")
        obj_class = globals()[item.capitalize()]  # Récupère la classe Cow ou Carrot en fonction de l'argument 'item'

        if item == "cow":
            SIZE = SIZE_COW
        elif item == "knife":
            SIZE = SIZE_KNIFE
        elif item == "carrot":
            SIZE = SIZE_CARROT
        elif item == "trap":
            SIZE = SIZE_TRAP

        if not getattr(self, exist_attr):
            for _ in range(Nbr):
                while True:
                    x = random.randint(0, len(self.sand_matrix) * CELL_SIZE) - 1
                    y = random.randint(0, len(self.sand_matrix) * CELL_SIZE) - 1
                    x_m, y_m = self.game_to_matrix_position(x, y)
                    rect = pygame.Rect(x, y, 20, 20)
                    if not any(rect.colliderect(wall) for wall in self.walls) and self.sand_matrix[x_m][y_m] > 0:
                        break

                new_item = obj_class(x, y, SIZE)
                group.add(new_item)
                setattr(self, exist_attr, True)
                print(f"{item}s displayed")
            group.update()

#-----------------------------------------------------------------------------------------------------------------------

    def update_item(self, life_change, item):

        interaction = f"interaction_{item}"
        group = getattr(self, f"{item}_group")
        if getattr(self, interaction):
            if item == "trap":
                self.interaction_trap = False
                self.player.life = 0
                return
            if item == "knife":
                new_images = {
                    "face": [pygame.image.load(f'Map/Designs_candy/Marche massue/Face/Anim_Face_massue-{i}.png') for i in
                             range(1, 4)],
                    "dos": [pygame.image.load(f'Map/Designs_candy/Marche massue/dos/Anim_Dos_massue-{i}.png') for i in range(1, 4)],
                    "gauche": [pygame.image.load(f'Map/Designs_candy/Marche massue/Gauche/Anim_Gauche_massue-{i}.png') for i in
                               range(1, 4)],
                    "droite": [pygame.image.load(f'Map/Designs_candy/Marche massue/Droite/Anim_Droite_massue-{i}.png') for i in
                               range(1, 4)]
                }
                self.player.update_walk_images(new_images)
                self.player.add_to_inventory("knife")
                for item_obj in group:
                    item_obj.respawn(10000, 10000)
                    break
                setattr(self, interaction, False)
                return
            
            if item=="carrot":
                for item_obj in self.carrot_group:
                    item_obj.respawn(7000, 7000)
                    break
                for i in range(1,4):
                    self.player.image = pygame.image.load(f'Map/Designs_candy/Glace/Anim Glace/Anim_Glace-{i}.png')
                    self.player.image = pygame.transform.scale(self.player.image, (SIZE_PLAYER, SIZE_PLAYER))
                    self.update_screen()
                    self.player.life += life_change/3
                    pygame.time.delay(500) 

            if item == "cow":
                self.player.remove_from_inventory("knife")

                for item_obj in self.cow_group:
                    item_obj.cow_flag=1
                    for i in range(1,4):
                        for j in range(1,5):
                            self.player.image = pygame.image.load(f'Map/Designs_candy/Marche massue/Coup/Coup_Massue-{j}.png')
                            self.player.image = pygame.transform.scale(self.player.image, (SIZE_PLAYER, SIZE_PLAYER))
                            self.update_screen()
                            pygame.time.delay(10)

                        item_obj.image = pygame.image.load(f'Map/Designs_candy/Vache/Mort/Vache-{i}.png')
                        item_obj.image = pygame.transform.scale(item_obj.image, (SIZE_COW, SIZE_COW))
                        self.update_screen()
                        self.player.life += life_change/3   
                                     

                self.player.images = {
                    'face': [pygame.image.load(f'Map/Designs_candy/Marche/Face/Anim_Face-{i}.png') for i in range(1, 4)],
                    'dos': [pygame.image.load(f'Map/Designs_candy/Marche/Dos/Anim_Dos-{i}.png') for i in range(1, 4)],
                    'gauche': [pygame.image.load(f'Map/Designs_candy/Marche/Gauche/Anim_Gauche-{i}.png') for i in range(1, 4)],
                    'droite': [pygame.image.load(f'Map/Designs_candy/Marche/Droite/Anim_Droite-{i}.png') for i in range(1, 4)]
                }
                self.player.update_walk_images(self.player.images)
                setattr(self, interaction, False)
                while True:
                    x = random.randint(0, len(self.sand_matrix) * CELL_SIZE) - 1
                    y = random.randint(0, len(self.sand_matrix) * CELL_SIZE) - 1
                    x_m, y_m = self.game_to_matrix_position(x, y)
                    rect = pygame.Rect(x, y, 20, 20)
                    if not any(rect.colliderect(wall) for wall in self.walls) and (self.sand_matrix[x_m][y_m] > 0):
                        break
                for item_obj in self.knife_group:
                    item_obj.respawn(x, y)
                    break

            for item_obj in group:
                if item=="cow":
                    item_obj.cow_flag=0
                while True:
                    x = random.randint(0, len(self.sand_matrix) * CELL_SIZE) - 1
                    y = random.randint(0, len(self.sand_matrix) * CELL_SIZE) - 1
                    x_m, y_m = self.game_to_matrix_position(x, y)
                    rect = pygame.Rect(x, y, 20, 20)
                    if not any(rect.colliderect(wall) for wall in self.walls) and (self.sand_matrix[x_m][y_m] > 0):
                        break
                item_obj.respawn(x, y)
                break
            setattr(self, interaction, False)
            self.player.life += life_change

            

#-----------------------------------------------------------------------------------------------------------------------

    def draw_item(self, item):
        # Dessinez chaque élément dans le groupe de sprites sur la surface de jeu
        group = getattr(self, f"{item}_group")
        for obj in group:
            self.group.add(obj)

#-----------------------------------------------------------------------------------------------------------------------

    def collision_item(self, item, key):
        # Mettre à jour la position du personnage en cas de collision
        self.group.update()
        for obj in getattr(self, f"{item}_group"):
            if item == "cow":
                if obj.rect.colliderect(self.player.rect) and self.pressed[key] and self.player.check_inventory("knife"):
                    setattr(self, f"interaction_{item}", True)
                    return obj
            elif item == "trap":
                if obj.rect.colliderect(self.player.feet):
                    setattr(self, f"interaction_{item}", True)
                    return obj
            else:
                if obj.rect.colliderect(self.player.rect) and self.pressed[key]:
                    setattr(self, f"interaction_{item}", True)
                    return obj

#-----------------------------------------------------------------------------------------------------------------------

    def game_over(self):
        """
        Function to display game over message and quit the game
        """
        self.player.image = pygame.image.load(f'Map/Designs_candy/Marche/Mort.png')
        self.player.image = pygame.transform.scale(self.player.image, (SIZE_PLAYER, SIZE_PLAYER))
        for trap in self.trap_group:
            trap.change_image(
                'Map/Designs_candy/Piège/Piège-2.png')

        self.update_screen()

        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()
        pygame.time.delay(3000)
        self.player.death()

#-----------------------------------------------------------------------------------------------------------------------
    
    def run(self):
        """
        While running loop to call all the functions until the user quit the game window.
        :return: void
        """
        clock = pygame.time.Clock()
        running = True

        while running:
            self.pressed = pygame.key.get_pressed()

            self.player.save_location()
            self.handle_input()
            self.collisions()
            self.collisions_water()
            self.player.update()
            self.player.life_update()
            self.update_screen()

            # Check if player's life is zero
            if self.player.life <= 0:
                self.game_over()

            # Carrots
            if not self.carrot_group:
                self.spawn_item(1, "carrot")
            self.draw_item("carrot")
            self.collision_item("carrot", pygame.K_SPACE)  # carrots collision
            self.update_item(5, "carrot")  # carrots update after collision

            # Cows
            if not self.cow_group:
                self.spawn_item(1, "cow")
            self.draw_item("cow")
            self.collision_item("cow", pygame.K_SPACE)  # cows collision
            self.update_item(20, "cow")  # cow update after collision
            # Knife
            if not self.knife_group:
                self.spawn_item(1, "knife")
            self.collision_item("knife", pygame.K_SPACE)
            self.update_item(0, "knife")
            self.draw_item("knife")

            # Trap
            if not self.trap_group:
                self.spawn_item(3, "trap")
            self.draw_item("trap")
            self.collision_item("trap", None)
            self.update_item(0, "trap")

            # tick() used to control the number of time the code go through the while loop every seconds - 120 FPS
            clock.tick(60)
        pygame.quit()
