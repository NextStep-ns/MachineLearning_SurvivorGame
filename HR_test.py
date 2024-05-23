import pygame
import pyscroll
import pytmx

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Exemple de carte Tiled avec Pygame")

# Chargement de la carte Tiled (TMX)
tmx_data = pytmx.util_pygame.load_pygame("tiled/map.tmx")

# Création du moteur de rendu de la carte
map_data = pyscroll.data.TiledMapData(tmx_data)
map_layer = pyscroll.orthographic.BufferedRenderer(map_data, screen.get_size())

zoom_level = min(SCREEN_WIDTH / map_layer.map_rect.width, SCREEN_HEIGHT / map_layer.map_rect.height)
map_layer.zoom = zoom_level

# Création du groupe de sprites
group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

# Boucle principale
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mise à jour de l'affichage
    group.update()
    group.center((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    group.draw(screen)

    # Rafraîchissement de l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()