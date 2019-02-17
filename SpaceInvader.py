"""
Space Invader
Made by Gainsboroow
Github : https://github.com/Gainsboroow/
Github Repository : https://github.com/Gainsboroow/Space-Invaders

How to play :
Arrows to move
Space to shoot

If the game is too slow, you can change the factor variable below,
1/2 will make the game 2 times faster, 1/3 3 times faster, etc.

Enjoy !
"""
factor = 1

from random import *
import pygame
from pygame.locals import *
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial Black', 60)

height, width = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space invaders")

nbPas = 10
delta = 10
frame = 0

class Caracter():
    def __init__(self, x,y):
        self.surfaces = [enemyImage, enemyImage2]
        self.rect = enemyImage.get_rect()
        self.rect.x, self.rect.y = x, y
        self.nbPas = 0
        self.delta = delta
        self.indexSurface = 0
        self.dead = False

    def update(self):
        self.indexSurface = 1 - self.indexSurface
        if self.nbPas == nbPas:
            self.nbPas = 0
            self.rect.move_ip(0,self.rect.height)
            self.delta *= -1
        else:
            self.nbPas += 1
            self.rect.move_ip(self.delta,0)

    def check(self):
        index = self.rect.collidelist(myBullets)
        if index != -1:
            self.dead = True
            del myBullets[index]
        return index

    def shoot(self):
        bullets.append( pygame.Rect(self.rect.centerx, self.rect.centery, 3, 10) )

    def display(self):
        screen.blit(self.surfaces[self.indexSurface], self.rect)

def startGame():
    myfont = pygame.font.SysFont('Arial', 30)
    textsurface = [myfont.render("Space invaders game", True, (255,255,255)),
                   myfont.render("Use arrows to move and Space to shoot", True, (255,255,255)),
                   myfont.render("Press any key to start", True, (255,255,255)) ]
    
    for i, txt in enumerate(textsurface):
        screen.blit(txt, (0,i*50))
    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                return 

def endGame(msg, color):
    textsurface = myfont.render(msg, True, color)
    screen.blit(textsurface,(100,height//2))
    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

startGame()

enemyImage = pygame.image.load("enemy.png").convert()
enemyImage2 = pygame.image.load("enemy2.png").convert()
enemies = []
bullets = []

me = pygame.Rect(width // 2, height - 30, 70, 10)
myBullets = []
nextShot = -1
enVie = 0

for x in range(30, width - nbPas*delta - 28, 50):
    for y in range(30, height // 4, 30):
        enemies.append( Caracter(x,y) )
        enVie += 1

clock = pygame.time.Clock()

while 1:
    keys = pygame.key.get_pressed()

    if keys[K_LEFT]:
        me.move_ip(-1/factor,0)
    if keys[K_RIGHT]:
        me.move_ip(1/factor,0)

    if keys[K_SPACE] and frame > nextShot:
        myBullets.append( pygame.Rect(me.centerx, me.centery, 3, 10) )
        nextShot = frame + 60*factor

    if me.left < 0:
        me.left = 0
    if me.right > width:
        me.right = width

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    screen.fill((0,0,0))

    for enemy in enemies:
        if enemy.dead : continue
        if enemy.check() != -1: 
            enVie -= 1

        if not(frame%(60*factor)):
            enemy.update()
            if random() < 0.05:
                enemy.shoot()
        else:
            enemy.display()

        if enemy.rect.bottom > height:
            endGame("Game Over", (255,0,0))
        

    for bullet in bullets:
        pygame.draw.rect(screen, (255,255,255), bullet)
        #if not( frame % 10 ):
        bullet.move_ip(0, 1/factor)
    
    for bullet in myBullets:
        pygame.draw.rect(screen, (0,255,0), bullet)
        bullet.move_ip(0, -1/factor)

    if me.collidelist(bullets) != -1:
        endGame("Game Over", (255,0,0))
    if enVie == 0:
        endGame("You won !", (0,255,0))



    pygame.draw.rect(screen, (0,255,0), me)
    pygame.display.flip()
    frame += 1
    clock.tick(60)
