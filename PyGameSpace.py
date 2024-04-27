#############################################################################################################
#                                                                                                           #
#                                            Treffe den Feind!                                              #
#                                              - mimi game -                                                #
#                                                                                                           #
#############################################################################################################

#############################################################################################################
#                                                                                                           #
#                                                MODULES                                                    #
#                                                                                                           #
#############################################################################################################
import pygame
import random

#############################################################################################################
#                                                                                                           #
#                                                 SURFACE                                                   #
#                                                                                                           #
#############################################################################################################

#GAME SETTINGS   
game_name = "Space invador"
background_image = "Hintergrund All 2.jpg"
WIDTH, HEIGHT = 600, 400
frames = 60
#COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialisierung des Bildschirms



#############################################################################################################
#                                                                                                           #
#                                                 ACTORS                                                    #
#                                                                                                           #
#############################################################################################################

#PLAYER
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 20
PLAYER_SPEED = 5

#ENEMY
ENEMY_WIDTH, ENEMY_HEIGHT = 30, 30
ENEMY_SPEED = 3
ENEMY_INTERVAL = 60  # Intervall, in dem ein neuer Gegner erscheint

#############################################################################################################
#                                                                                                           #
#                                                 ACTORS                                                    #
#                                                                                                           #
#############################################################################################################


#############################################################################################################
#                                                                                                           #
#                                                FUNKTIONS                                                  #
#                                                                                                           #
#############################################################################################################

# Funktion zum Erstellen der Spielwelt
def set_world(width,height,caption,image,fps):
    global clock
    global screen
    global background
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)    
    image = pygame.image.load(image).convert()
    background = pygame.transform.scale(image,(width,height))
    clock = pygame.time.Clock()   
    clock.tick(fps)

# Funktion zum Zeichnen des Spielers
def draw_player(player):
    pygame.draw.rect(screen, RED, player)

# Funktion zum Zeichnen der Gegner
def draw_enemies(enemies, colour):
    for enemy in enemies:
        pygame.draw.rect(screen, colour, enemy)

# Funktion zum Erzeugen eines neuen Gegners
def create_enemy():
    x = random.randint(0, WIDTH - ENEMY_WIDTH)
    y = 0 - ENEMY_HEIGHT
    return pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)

# Funktion zum Bewegen der Gegner
def move_enemies(enemies):
    for enemy in enemies:
        enemy.y += ENEMY_SPEED


# Funktion zum Zeichnen der Gegner
def draw_enemies(enemies,colour):
    for enemy in enemies:
        pygame.draw.rect(screen, colour, enemy)


#############################################################################################################
#                                                                                                           #
#                                                 MAIN CODE                                                 #
#                                                                                                           #
#############################################################################################################

def main():
    player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - 50, PLAYER_WIDTH, PLAYER_HEIGHT)
    enemies = []
    mouse_x = 0 
    mouse_y = 0
    pygame.init()
    set_world(WIDTH,HEIGHT,game_name,background_image,frames) 
    running = True
    while running:
        screen.blit(background,(0,0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player.x += PLAYER_SPEED
       
        

        # Begrenze den Spieler auf den Bildschirm
        player.x = max(0, min(player.x, WIDTH - PLAYER_WIDTH))

        # Bewege die Gegner und füge neue hinzu
        move_enemies(enemies)
        if random.randint(0, ENEMY_INTERVAL) == 0:
            enemies.append(create_enemy())

        # Kollisionserkennung
        for enemy in enemies:
            if player.colliderect(enemy):
                running = False

        # Zeichne Spieler und Gegner
        draw_player(player)
        draw_enemies(enemies,WHITE)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

