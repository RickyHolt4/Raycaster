import pygame
import math
import random
pygame.init()

winWidth, winHeight = (1920, 1080)
window = pygame.display.set_mode((winWidth, winHeight))

class Camera:
    def __init__(self, fov, tm, x, y):
        self.colors = [
            [0,0,0],#Black
            [255,0,0],#red
            [255, 155, 0],#orange
            [255, 255, 0],#Yellow
            [0, 255, 0],#Green
            [0, 255, 255],#Light Blue
            [0, 0, 255],#Blue
            [255, 0, 255]#violet
        ]
        self.fov = fov
        self.view = 0
        self.tm = tm
        self.distances = []
        self.x = x
        self.y = y
        self.movements = {"Forward":False, "Backwards":False, "Left":False, "Right":False}
        for y, row in enumerate(self.tm):
            for x, tile in enumerate(row):
                if tile != 0:
                    self.tm[y][x] = random.randint(1,7)
    def draw(self, window):
        #Actual
        for x, line in enumerate(self.distances): 
            height = round(256 / line[0])
            pygame.draw.rect(window, (255-(line[0]*20),255-(line[0]*20),255-(line[0]*20)), (x*int(1920/(self.fov*2)), 512-height, int(1920/(self.fov*2)), height*2))
        #Minimap
        pygame.draw.circle(window, (255,0,0), (self.x*32, self.y*32), 4)
        for y, row in enumerate(self.tm):
            for x, tile in enumerate(row):
                if tile != 0:
                    pygame.draw.rect(window, self.colors[0], (x*32, y*32, 32, 32))
    def update(self):
        radAngle = math.radians(self.view+(self.fov/2))
        if self.movements["Forward"] == True and self.tm[int((math.sin(radAngle)*.05)+self.y)][int((math.cos(radAngle)*.05)+self.x)] == 0:
            self.x += math.cos(radAngle)*.05
            self.y += math.sin(radAngle)*.05
        if self.movements["Left"] == True:
            self.view -= 5
        if self.movements["Right"] == True:
            self.view += 5

    def distance(self, window):
        self.distances = []
        for i in range(self.fov*2):
            degree = (i/2)+self.view
            if degree > 360:
                degree = degree - 360
            if degree < 0:
                degree = 360 + degree
            
            rayx = self.x
            rayy = self.y
            radAngle = math.radians(degree)
            while self.tm[int(rayy)][int(rayx)] == 0:
                rayx += math.cos(radAngle)*.01
                rayy += math.sin(radAngle)*.01
                pygame.draw.rect(window, (0,255,0), (rayx*32, rayy*32, 1, 1))
            dist = math.sqrt(((rayx-self.x)*(rayx-self.x)+(rayy-self.y)*(rayy-self.y)))
            viewingAngle = self.view+(self.fov/2)
            angle = viewingAngle-degree
            dist = dist*math.cos(math.radians(angle))
            color = self.colors[self.tm[int(rayy)][int(rayx)]]
            self.distances.append((dist, color))
                
class Control:
    def __init__(self):
        self.run = True
        self.clock = pygame.time.Clock()
    
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.movements["Forward"] = True
                if event.key == pygame.K_a:
                    player.movements["Left"] = True
                if event.key == pygame.K_d:
                    player.movements["Right"] = True
                if event.key == pygame.K_ESCAPE:
                    self.run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.movements["Forward"] = False
                if event.key == pygame.K_a:
                    player.movements["Left"] = False
                if event.key == pygame.K_d:
                    player.movements["Right"] = False

tm = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]
player = Camera(32, tm, 1.5, 2.5)
control = Control()
while control.run:
    window.fill((100,100,100))
    player.draw(window)
    player.distance(window)
    pygame.display.update()
    control.update()
    player.update()
    control.clock.tick(15)

pygame.quit()