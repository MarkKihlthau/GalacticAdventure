import pygame
import random
import time

pygame.init()

# Create Window
X_max = 800
Y_max = 600
screen = pygame.display.set_mode((X_max, Y_max))

# Background Image
backgroundImg = pygame.image.load('SpaceBackground.png')

# Title
pygame.display.set_caption("Galactic Adventure")

# Kill Counter
font = pygame.font.Font('freesansbold.ttf', 32)
green = (0, 255, 0)
blue = (0, 0, 128)
kill_count = 0
text = font.render(('Kills: ' + str(kill_count)), True, green, blue)
textRect = text.get_rect()
textRect.center = (100, 550)

# Try Again Prompt
try_again_font = pygame.font.Font('freesansbold.ttf', 32)
try_again_text = font.render("You Died. Press Space to Continue", True, green, blue)
try_again_textRect = try_again_text.get_rect()
try_again_textRect.center = (400, 300)

# Player
playerImg = pygame.image.load('SpaceShip.png')
playerX = 400
playerY = 300
playerAlive = True

# Bullet
bulletImg = pygame.image.load('Bullet.png')
player_bullet_list = []
class Player_bullet:
    def __init__(self, img, x, y, hit):
        self.img = img
        self.x = x
        self.y = y
        self.hit = hit


# Enemy List
enemy_list = []
enemy_count = 0
enemy_speed = 0.3


# Enemy Bullet List
enemyBulletImg = pygame.image.load('Enemy_Bullet.png')
enemy_bullet_list = []
enemy_bullet_speed = 0.5


# Enemy Class
class Enemy:
    def __init__(self, img, x, y, alive, bounce, id_num):
        self.img = img
        self.x = x
        self.y = y
        self.alive = alive
        self.bounce = bounce
        self.id_num = id_num


# Enemy Bullet Class
class Enemy_bullet:
    def __init__(self, img, x, y):
        self.img = img
        self.x = x
        self.y = y


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(img, x, y):
    screen.blit(img, (x, y))


def fill_background(x_size, y_size, movement):
    x = 0
    y = -500
    while y < y_size:
        screen.blit(backgroundImg, (x, y + movement))
        x += 64
        if x >= x_size:
            y += 64
            x = 0


def fire(x, y):
    screen.blit(bulletImg, (x, y))


def spawn():
    spawn_point = random.randint(1, 6)
    if spawn_point == 1:
        enemy_list.append(Enemy(pygame.image.load('Enemy.png'), 0, 0, True, False, enemy_count))
    elif spawn_point == 2:
        enemy_list.append(Enemy(pygame.image.load('Enemy.png'), 0, 64, True, False, enemy_count))
    elif spawn_point == 3:
        enemy_list.append(Enemy(pygame.image.load('Enemy.png'), 0, 128, True, False, enemy_count))
    elif spawn_point == 4:
        enemy_list.append(Enemy(pygame.image.load('Enemy.png'), X_max-64, 0, True, False, enemy_count))
    elif spawn_point == 5:
        enemy_list.append(Enemy(pygame.image.load('Enemy.png'), X_max-64, 64, True, False, enemy_count))
    elif spawn_point == 6:
        enemy_list.append(Enemy(pygame.image.load('Enemy.png'), X_max-64, 128, True, False, enemy_count))


def enemy_fire(x, y):
    screen.blit(enemyBulletImg, (x, y))


running = True
background_animation = 0

spawn()
enemy_count += 1
start = time.time()
spawn_t1 = time.time()
spawn_count = 0
spawning = False
spawned = 0
print("Enemy Count: ", enemy_count)

# Game Loop
while running:
    screen.fill((0, 0, 0))
    background_animation += 0.5
    if background_animation > 100:
        background_animation = 0
    fill_background(X_max, Y_max, background_animation)

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and 0 <= playerX:
        playerX -= 1
    if keys[pygame.K_d] and playerX <= X_max-64:
        playerX += 1
    if keys[pygame.K_w] and 0 <= playerY:
        playerY -= 1
    if keys[pygame.K_s] and playerY <= Y_max-64:
        playerY += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_bullet_list.append(Player_bullet(bulletImg, playerX, playerY, False))
            if event.key == pygame.K_p:
                spawn()
                enemy_count += 1
                print("Enemy Count: ", enemy_count)

    player(playerX, playerY)

    for obj in player_bullet_list:
        # draw and move bullet
        if obj.y > 0 and obj.hit is False:
            fire(obj.x, obj.y)
            obj.y -= 2
        else:
            # delete bullet
            length = len(player_bullet_list)
            for i in range(length):
                if player_bullet_list[i-1].y <= 0 or player_bullet_list[i-1].hit is True:
                    player_bullet_list.pop(i-1)

    for bullet in player_bullet_list:
        for obj in enemy_list:
            if obj.x-64 <= bullet.x <= obj.x+64 and obj.y-64 <= bullet.y <= obj.y+64:
                obj.alive = False
                bullet.hit = True
                kill_count += 1
                enemy_count -= 1
                print("Enemy Count: ", enemy_count)
                length = len(enemy_list)
                for i in range(length):
                    if enemy_list[i-1].x == obj.x and enemy_list[i-1].y == obj.y:
                        enemy_list.pop(i-1)

    for obj in enemy_list:
        if obj.y < 350 and obj.alive is True:
            if 0 < obj.x < X_max-64 and obj.bounce is False:
                obj.x += enemy_speed
            elif obj.x >= X_max-64:
                obj.bounce = True
                obj.y += 64
                obj.x -= enemy_speed
            elif 0 < obj.x < X_max-64 and obj.bounce is True:
                obj.x -= enemy_speed
            elif obj.x <= 0:
                obj.bounce = False
                obj.y += 64
                obj.x += enemy_speed

    for obj in enemy_list:
        if obj.alive is True:
            enemy(obj.img, obj.x, obj.y)

    for obj in enemy_list:
        end = time.time()
        if (end - start) > 1:
            rand_fire = random.randint(0, 1)
            if rand_fire == 1:
                enemy_bullet_list.append(Enemy_bullet(enemyBulletImg, obj.x, obj.y))
            start = time.time()

    for obj in enemy_bullet_list:
        enemy_fire(obj.x, obj.y)
        obj.y += enemy_bullet_speed
        if obj.x - 64 <= playerX <= obj.x + 64 and obj.y - 64 <= playerY <= obj.y + 64:
            playerAlive = False

    text = font.render(('Kills: ' + str(kill_count)), True, green, blue)
    screen.blit(text, textRect)

    if enemy_count == 0:
        spawning = True
        spawn_count = random.randint(1, 6)
        spawned = 0

    if spawning is True:
        for i in range(spawn_count):
            spawn_t2 = time.time()
            if spawn_t2 - spawn_t1 > 1:
                spawn()
                enemy_count += 1
                spawned += 1
                print("Enemy Count: ", enemy_count)
                spawn_t1 = time.time()

    if spawned == spawn_count:
        spawning = False

    # Game Over
    if playerAlive is False:
        screen.fill((0, 0, 0))
        screen.blit(try_again_text, try_again_textRect)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playerAlive = True

    pygame.display.update()

