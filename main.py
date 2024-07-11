import random
import os

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT



pygame.display.set_caption("Ураїнський Байрактар")
pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 700
WIDTH = 1350
HEIGHT_enemy = random.randint(250, 600)
WIDTH_bonus = random.randint(900, 2000)

FONT = pygame.font.SysFont('Verdana', 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH,HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player_size = (20, 20)
player = pygame.image.load('player.png').convert_alpha()#pygame.Surface(player_size)
# player.fill(COLOR_BLACK)
player_rect = player.get_rect()
player_rect.x = 150
player_rect.y = 250
# player_speed = [1, 1]
player_move_down = [0, 9]
player_move_right = [9, 0]
player_move_left = [-9, -0]
player_move_top = [0, -9]

def create_bonus():
    bonus_size = (30, 80)
    bonus = pygame.image.load('bonus.png').convert_alpha()#pygame.Surface(bonus_size)
    bonus_size = bonus.get_size()
    bonus = pygame.transform.scale(bonus, (100, 150))
    # bonus.fill(COLOR_GREEN)
    bonus_rect = pygame.Rect(random.randint(0, WIDTH_bonus), 0, *bonus_size) 
    bonus_move = [0, random.randint(7, 9),]
    return [bonus, bonus_rect, bonus_move]


CREATE_BONUS = pygame.USEREVENT +1
pygame.time.set_timer(CREATE_BONUS, 1500)
bonuses = []


def create_enemy():
    enemy_size = (30, 30)
    enemy = pygame.image.load('enemy.png').convert_alpha()#pygame.Surface(enemy_size)
    enemy_size = enemy.get_size()
    enemy = pygame.transform.scale(enemy, (100, 50))
    # enemy.fill(COLOR_BLUE)
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT_enemy), *enemy_size)
    enemy_move = [random.randint(-6, -5), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT +2
pygame.time.set_timer(CREATE_ENEMY, 2500)
enemies = []

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)
image_index = 0

score = 0
image_index = 0

playing = True

while playing:
    FPS.tick(150)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    # main_display.fill (COLOR_BLACK)            
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()


    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right) 

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    if keys[K_UP] and player_rect.top >= 0:
        player_rect = player_rect.move(player_move_top)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy [1]):
            playing = False


    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus [1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

      
    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
    main_display.blit(player, player_rect)
    
    

    
    pygame.display.flip()

    for enemy in enemies:
        if enemy[1]. left < 0:
            enemies.pop(enemies.index(enemy))
            
    for bonus in bonuses:
        if bonus[1]. bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
        


        