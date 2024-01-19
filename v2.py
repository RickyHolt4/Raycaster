import pygame
import math

pygame.init()

winWidth, winHeight = (768, 512)
window = pygame.display.set_mode((winWidth, winHeight))
pygame.mouse.set_visible(False)
class Player:
    def __init__(self, x, y, tm, fov, view, enemys):
        self.x = x
        self.y = y
        self.tm = tm
        self.fov = fov
        self.view = view
        self.movements = {'w': False, 'a':False, 's':False, 'd':False}
        self.distances = []
        self.enemys = enemys
        self.img = pygame.image.load("tile_test.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (64, 64))
        self.mid = 256
        self.floors = []
        self.floors_x = []
        self.floors_y = []

    
    def update(self):
        radAngle = math.radians(self.view)
        radAngleLeft = math.radians(self.view - 90)
        radAngleRight = math.radians(self.view + 90)

        if self.movements['w'] == True and self.tm[int(self.y+(math.sin(radAngle)*0.05))][int(self.x+(math.cos(radAngle)*0.05))] == 0:
            self.x += math.cos(radAngle)*0.05
            self.y += math.sin(radAngle)*0.05
        if self.movements['a'] == True and self.tm[int(self.y+(math.sin(radAngleLeft)*0.05))][int(self.x+(math.cos(radAngleLeft)*0.05))] == 0:
            self.x += math.cos(radAngleLeft)*0.05
            self.y += math.sin(radAngleLeft)*0.05
        if self.movements['s'] == True and self.tm[int(self.y-(math.sin(radAngle)*0.05))][int(self.x-(math.cos(radAngle)*0.05))] == 0:
            self.x -= math.cos(radAngle)*0.05
            self.y -= math.sin(radAngle)*0.05
        if self.movements['d'] == True and self.tm[int(self.y+(math.sin(radAngleRight)*0.05))][int(self.x+(math.cos(radAngleRight)*0.05))] == 0:
            self.x += math.cos(radAngleRight)*0.05
            self.y += math.sin(radAngleRight)*0.05

        mx, my = pygame.mouse.get_pos()
        dx = mx - 384
        dy = 256 - my
        self.view += dx
        #self.mid += dy*4
        if self.mid < -512:
            self.mid = -512
        elif self.mid > 1024:
            self.mid = 1024
        pygame.mouse.set_pos(384, 256)
        
        
        

            
    def draw(self, window):
        #Rays :D
        self.distances = []
        self.floors = []
        self.floors_x = []
        self.floors_y = []

        for dy in range(-self.fov//2, self.fov//2):
            degree = self.view + math.degrees(math.atan2(dy, 50))
            radAngle = math.radians(degree)
            rayx = self.x
            rayy = self.y
            
            stop = False
            while self.tm[int(rayy)][int(rayx)] == 0 and stop == False:
                rayx += math.cos(radAngle)*0.01
                rayy += math.sin(radAngle)*0.01

                dist = math.sqrt(((rayx-self.x)*(rayx-self.x)+(rayy-self.y)*(rayy-self.y)))


            dist *= math.cos(math.radians(degree - self.view))
            

            

            
            #player view
            #pygame.draw.line(window, (255,0,0), (self.x*8, self.y*8), ((self.x+math.cos(math.radians(self.view)))*8, (self.y+math.sin(math.radians(self.view)))*8))
            #pygame.draw.line(window, (255,0,0), (self.x*8, self.y*8), ((self.x+math.cos(math.radians(self.view-(self.fov/2))))*8, (self.y+math.sin(math.radians(self.view-(self.fov/2))))*8))
            #pygame.draw.line(window, (255,0,0), (self.x*8, self.y*8), ((self.x+math.cos(math.radians(self.view+(self.fov/2))))*8, (self.y+math.sin(math.radians(self.view+(self.fov/2))))*8))
            #pygame.draw.line(window, (255,0,0), (self.x*8, self.y*8), ((self.x+math.cos(math.radians(self.view-(self.fov/4))))*8, (self.y+math.sin(math.radians(self.view-(self.fov/4))))*8))
            #pygame.draw.line(window, (255,0,0), (self.x*8, self.y*8), ((self.x+math.cos(math.radians(self.view+(self.fov/4))))*8, (self.y+math.sin(math.radians(self.view+(self.fov/4))))*8))

            #Decide if colides horizontslly or vertically
            rx = round(rayx - int(rayx), 5)
            ry = round(rayy - int(rayy), 5)
            h_col = False
            if rx > .5:
                if ry > .5 - (rx - .5) and ry < .5 + (rx - .5):
                    h_col = True
                else:
                    h_col = False
            elif rx <= .5:
                if ry > .5 - (.5 - rx) and ry < .5 + (.5 - rx):
                    h_col = True
                else:
                    h_col = False
            
            if h_col == True:
                num = ry
            else:
                num = rx
            
            

            floor_y = self.y+math.sin(radAngle)*dist
            self.distances.append((dist, num, floor_y))
        
        #---3D View---
        #Walls
        for x, line in enumerate(self.distances):
            height = round(256 / line[0])
            if height <= .5:
                height = .5
            w, h = self.img.get_width(), self.img.get_height()

            img_x = int(line[1]*w)
            if img_x > 63:
                img_x = 63
            elif img_x < 0:
                img_x = 0
            img_y = int(line[1]*h)
            if img_y > 63:
                img_y = 63
            elif img_y < 0:
                img_y = 0
            img = self.img.subsurface(img_x, 0, 1, h)
            img = pygame.transform.scale(img, (12, height*2))

            window.blit(img, ((x*12), self.mid-height))
            #Floor
            

            



                

        #---TopDown View---
        #Map
        for y, row in enumerate(self.tm):
            for x, tile in enumerate(row):
                if tile == 1:
                    pygame.draw.rect(window, (255,255,255), (x*8, y*8, 8, 8))
                else:
                    pygame.draw.rect(window, (0,0,0), (x*8, y*8, 8, 8))
        
        
        #player
        pygame.draw.circle(window, (255,255,0), (self.x*8, self.y*8), 2)
        


        
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
                    player.movements["w"] = True
                if event.key == pygame.K_a:
                    player.movements["a"] = True
                if event.key == pygame.K_s:
                    player.movements["s"] = True
                if event.key == pygame.K_d:
                    player.movements["d"] = True
                if event.key == pygame.K_ESCAPE:
                    self.run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.movements["w"] = False
                if event.key == pygame.K_a:
                    player.movements["a"] = False
                if event.key == pygame.K_s:
                    player.movements["s"] = False
                if event.key == pygame.K_d:
                    player.movements["d"] = False

game = Control()
tm = [
    [1,1,1,1,1,1,1,1],
    [1,0,1,0,0,0,0,1],
    [1,0,1,1,0,1,0,1],
    [1,0,0,0,0,1,0,1],
    [1,1,1,1,0,1,0,1],
    [1,0,1,1,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1]
]

player = Player(3.5, 3.5, tm, 64, 0, [])

while game.run:
    window.fill((0,255,0))
    pygame.draw.rect(window, (0,255,255), (0,0,768,player.mid))
    player.draw(window)

    pygame.display.update()
    game.update()
    player.update()
    

    game.clock.tick(30)

pygame.quit()