import pygame
import random
from pygame.locals import * # need this for userevent

# reference https://stackoverflow.com/questions/22119244/pygame-key-get-pressed-doesnt-work-pygame-error-video-system-not-initial

"""design
    1, ship shoots at enemies and screen scrolls
    2, enemies are big companies you aim to get into, they can emerge from any angle 
    3, you can call help when you reach certain points
    4, after certain points, you win

"""

pygame.init() # initialize py game

window = pygame.display.set_mode((1000,600)) # surface, topleft is 0,0 , bottm right is 500,500
pygame.display.set_caption("Star Wars")
bg = pygame.image.load("d7d97bc4-13a2-4a57-9895-8fdb9edd13a9_scaled.jpg")
char = pygame.image.load('spaceship.pod_.1.png')
bullet_sound = pygame.mixer.Sound("expl3.wav")
yelp = pygame.image.load("YelpIcon.png")

#window.blit(bg,(0,0))
#window.blit(char,(0,0))

window.blit(pygame.transform.scale(bg,(1000,600)),(0,0))
window.blit(pygame.transform.scale(char,(64,64)),(500,500))
#window.blit(yelp,(500,100))

pygame.display.update()

class Ship:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = False # helper ship
        self.hp = 10

class Enemy:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.nums = 0 # how many of them can appear at a time
        self.vel = 12
        self.hitbox = (self.x, self.y, 64, 64)

    def draw(self,window):
        window.blit(pygame.transform.scale(yelp, (48, 48)), (self.x, self.y))
        self.hitbox = (self.x, self.y , 48, 48) # hit box moves along with enemy,
        pygame.draw.rect(window, (250, 0, 0), self.hitbox, 2)
        #pygame.draw.circle(window, (250,0,0), (self.x, self.y),10)

    def collide(self,bullet):
        # bullet collides with enemies
        if self.hitbox[0] < bullet.x + bullet.radius and self.hitbox[0] + self.hitbox[2] > bullet.x:

             return True
        return False

class Bullets:
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 15

    def draw(self,window):
        pygame.draw.circle(window,self.color,(self.x,self.y),self.radius)
        # bullets.append(Bullets(ms.x + (ms.width // 2),ms.height,6,(0,0,0)))

def redraw():
    window.blit(pygame.transform.scale(bg, (1000, 600)), (0, 0))  # fix fps
    window.blit(pygame.transform.scale(char, (64, 64)), (ms.x, ms.y))

    for bullet in bullets:
        bullet.draw(window)

    for enemy in enemies:
        enemy.draw(window)

    #pygame.draw.rect(window, (250, 0, 0), (100,100,64,64), 2)

    pygame.display.update()

clock = pygame.time.Clock()
pygame.time.set_timer(USEREVENT+1,1000)
bullets = []
enemies = []
ms = Ship(500,500,64,64) # ms = mainship
enemy1 = Enemy(1000, 100, 64, 64)

vel = 10
run = True
while run:
    clock.tick(30)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

        # this is where Enemies are created
        if event.type == USEREVENT+1:
            for i in range(5):
                enemies.append(enemy1)

    for bullet in bullets:

        # if enemy.hitbox[0] + enemy.hitbox[2] > bullet.x and bullet.x + bullet.radius > enemy.hitbox[0]:
        # # if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
        # #     if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
        # #         #isHit = True
        #     print('hit')

        if 0 < bullet.y < 600: # make sure it is not out of boundary
            bullet.y -= bullet.vel

        else:
            bullets.remove(bullet)

    for enemy in enemies:

        if 0 < enemy.x + enemy.vel:
            enemy.x -= enemy.vel
            # how to move hitbox along with ship

        # if enemy.x < 500:
        #     enemy.y += enemy.vel

        else:
            enemies.remove(enemy)

        #pygame.draw.rect(window, (250, 0, 0), (ms.x, ms.y, 5, 5))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if len(bullets) < 10:
            bullets.append(Bullets(ms.x + (ms.width // 2),ms.y,6,(255,0,0)))
            bullet_sound.play()

    if keys[pygame.K_UP]:
        ms.y -= vel

    if keys[pygame.K_DOWN]:
        ms.y += vel

    if keys[pygame.K_LEFT]:
        ms.x -= vel

    if keys[pygame.K_RIGHT]:
        ms.x += vel

    redraw()

pygame.quit()