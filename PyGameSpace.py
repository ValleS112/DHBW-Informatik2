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
import math

#############################################################################################################
#                                                                                                           #
#                                                 SURFACE                                                   #
#                                                                                                           #
#############################################################################################################

#GAME SETTINGS   
game_name = "Space invador"
background_image = "Hintergrund All 2.jpg"

WORLD_WIDTH, WORLD_HEIGHT = 600, 400
frames = 60
#COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0,255,0)

# ACTOR SETTING
player_image = "Spaceship 1.png"
PLAYER_WIDTH, PLAYER_HEIGHT = 70, 70
PLAYER_RADIUS = 40
PLAYER_SPEED = 5

enemy_image = "UFO 1.png"
ENEMY_WIDTH, ENEMY_HEIGHT = 70, 70
ENEMY_RADIUS = 20
ENEMY_SPEED = 1
ENEMY_INTERVAL = 60  # Intervall, in dem ein neuer Gegner erscheint

#############################################################################################################
#                                                                                                           #
#                                                 CLASSES                                                   #
#                                                                                                           #
#############################################################################################################

#BASIC ACTOR
class Actor:
    def __init__(self, center_x, center_y, width, height, speed, appearance):
        self.position_x = center_x
        self.position_y = center_y
        self.speed = speed
        self.appearance = pygame.image.load(appearance).convert_alpha()
        self.appearance = pygame.transform.scale(self.appearance, (width, height))
        
    def move(self, speed_x, speed_y):
        self.position_x += speed_x
        self.position_y += speed_y
        
    def draw_body(self, surface, colour):
        for rect in self.body:
            pygame.draw.rect(surface,colour,rect, width=1)
        
    def draw_position(self, surface):
        pygame.draw.line(surface,RED,(self.position_x - 5, self.position_y),(self.position_x + 5, self.position_y))
        pygame.draw.line(surface,RED,(self.position_x, self.position_y - 5),(self.position_x, self.position_y +5))

class Player(Actor):
    def __init__(self, center_x, center_y, width, height, speed, appearance):
        super().__init__(center_x, center_y, width, height, speed, appearance)
        
        x = self.position_x
        y = self.position_y
        w = width
        h = height        
        self.body = [
            pygame.Rect(x-w/6,y-h/2,w/3,h/4),
            pygame.Rect(x-w/6,y-1/4*h,w/3,h/3),
            pygame.Rect(x-w/3,y+h/13,4/6*w,2/5*h),
            pygame.Rect(x-w/2,y+w/5,w,h/6),
            ]

    def move(self, speed_x, speed_y):
        super().move(speed_x, speed_y)
        
        if self.position_x >= (0+PLAYER_WIDTH/2) and self.position_x <= (WORLD_WIDTH-PLAYER_WIDTH/2):
            for rect in self.body:
                rect.x += speed_x

        if self.position_y >= (0+PLAYER_HEIGHT/2) and self.position_y <= (WORLD_HEIGHT-PLAYER_HEIGHT/2):
            for rect in self.body:
                rect.y += speed_y       
            
        self.position_x = max(0+PLAYER_WIDTH/2, min(self.position_x, WORLD_WIDTH-PLAYER_WIDTH/2))       
        self.position_y = max(0+PLAYER_HEIGHT/2, min(self.position_y, WORLD_HEIGHT-PLAYER_HEIGHT/2)) 

    

   

class Enemy(Actor):
    def __init__(self, center_x, center_y, width, height, speed, appearance):
        super().__init__(center_x, center_y, width, height, speed, appearance)
        x = self.position_x
        y = self.position_y
        w = width
        h = height        
        self.body = [
            pygame.Rect(x-2/7*w,y-1/25*h,3/5*w,1/8*h),
            pygame.Rect(x-1/7*w,y-1/5*h,2/7*w,2/5*h),
            ] 

    def move(self, speed_x, speed_y):
        super().move(speed_x,speed_y)
        
        for rect in self.body:
                rect.y += speed_y
   
        self.position_y = max(0, min(self.position_y, WORLD_HEIGHT+ENEMY_HEIGHT)) 

   

#############################################################################################################
#                                                                                                           #
#                                                FUNKTIONS                                                  #
#                                                                                                           #
#############################################################################################################

# Funktionen zum Erstellen der Spielwelt
def set_screen(width,height,caption,image,fps):
    global clock
    global screen
    global background
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)    
    image = pygame.image.load(image).convert()
    background = pygame.transform.scale(image,(width,height))
    clock = pygame.time.Clock()   
    clock.tick(fps)

def main_menue(surface):
    font_heading = pygame.font.Font(None, 70)
    font_menue = pygame.font.Font(None, 36)
    heading_surface = font_heading.render(heading, True, WHITE)
    menue_surface = font_menue.render(menue, True, WHITE)
    heading =  " SPACE INVADOR "
    menue = "Press SPACE to start"
    
    menue_surface = font_menue.render(menue, True, WHITE)
    menue_rect = menue_surface.get_rect().move(100, 100)
    heading_rect = heading_surface.get_rect(topleft = (5,10))
   
    menue_rect = menue_surface.get_rect(topleft = (100,100))

    screen.blit(heading, heading_rect)
    screen.blit(menue, menue_rect)


def set_player(center_x, center_y, width, height, speed, appearance):
    return Player(center_x, center_y, width, height, speed, appearance)
    
def set_enemy(x_position,y_position, width, height, speed, appearance):
    return Enemy(x_position, y_position, width, height, speed, appearance)

def create_enemy(rate):
    if random.randint(0,rate) == 0:
        enemy = set_enemy(random.randint(0+ENEMY_WIDTH, WORLD_WIDTH - ENEMY_WIDTH),0, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED, enemy_image)
        enemies.append(enemy)

def move_enemy(list):
    for enemy in enemies:
        screen.blit(enemy.appearance, (enemy.position_x-ENEMY_WIDTH/2-1, enemy.position_y-ENEMY_HEIGHT/2-5))
        # enemy.draw_position(screen)
        # enemy.draw_body(screen,RED)
    
    for enemy in enemies: 
        enemy.move(0,ENEMY_SPEED)
                    
    if len(list) >= 1:
        for enemy in list:
            if enemy.position_y == (WORLD_HEIGHT):
                list.remove(enemy)

def hud_menue():
    font = pygame.font.Font(None, 36)
    highscore_txt =  " Highscore: "
    text_surface = font.render(highscore_txt+str(int(score)), True, WHITE)
    text_rect = text_surface.get_rect(topleft = (5,10))
    screen.blit(text_surface, text_rect)

def key_event():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move((-1)*player.speed,0)
    if keys[pygame.K_RIGHT]:
        player.move(player.speed,0)
    if keys[pygame.K_UP]:
        player.move(0,(-1)*player.speed)
    if keys[pygame.K_DOWN]:
        player.move(0,player.speed)

def collision_event(obj1,obj2):
    collision = False
    for rect1 in obj1:
        for rect2 in obj2:
            if rect1.colliderect(rect2):
                collision = True
            
    if collision == True:
        font = pygame.font.Font(None, 36)
        highscore_txt =  " CRASH "
        text_surface = font.render(highscore_txt, True, RED)
        text_rect = text_surface.get_rect(center = (WORLD_WIDTH//2, WORLD_HEIGHT//2))
        screen.blit(text_surface, text_rect)

def score_counter(counter, score):
    score += counter
    return score

#############################################################################################################
#                                                                                                           #
#                                                 MAIN CODE                                                 #
#                                                                                                           #
#############################################################################################################

pygame.init()
set_screen(WORLD_WIDTH,WORLD_HEIGHT,game_name,background_image,frames)
main = True

while main:
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main = False
    screen.blit(background,(0,0))
    main_menue(screen)
    start = pygame.key.get_pressed()
    if start[pygame.K_SPACE]:
        player = set_player((WORLD_WIDTH/2), (WORLD_HEIGHT-PLAYER_HEIGHT), PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, player_image)
        enemies = []  
        score = 0

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.blit(background,(0,0))
            screen.blit(player.appearance, (player.position_x-PLAYER_WIDTH/2-1, player.position_y-PLAYER_HEIGHT/2))
            # player.draw_position(screen)
            # player.draw_body(screen,GREEN)
            hud_menue()
            score = score_counter(1/30, score)
            key_event()
            
            create_enemy(ENEMY_INTERVAL)     
            move_enemy(enemies)
            for enemy in enemies:
                collision_event(player.body,enemy.body) 
            
            pygame.display.flip()
            clock.tick(60)
    pygame.display.flip()        
pygame.quit()
    
    

