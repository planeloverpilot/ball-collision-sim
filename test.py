import pygame
import math
import random

pygame.init()
width, height = 1200, 690
display_surface = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
class Ball():
    def __init__(self, x, y, radius,vel,velx,mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = vel
        self.velx=velx
        self.mass=mass
        
    def move(self):
        self.vel += 0.98
        self.y += self.vel
        self.x +=self.velx
        if self.y + self.radius > height:
            self.y = height - self.radius
            self.vel = -self.vel * 0.89
        if self.x + self.radius > width:
            self.x = display_surface.get_width() - self.radius
            self.velx =- self.velx * 0.94
        if self.x - self.radius < 0:
            self.x = self.radius
            self.velx = -self.velx * 0.91
            
    def draw(self):
         pygame.draw.circle(display_surface, (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)), (int(self.x), int(self.y)), self.radius)
         
    def checkcol(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance < (self.radius + other.radius) and distance != 0:
    
            overlap = 0.5 * (self.radius + other.radius - distance +0.5)
            angle = math.atan2(dy, dx)
            self.x += math.cos(angle) * overlap
            self.y += math.sin(angle) * overlap
            other.x -= math.cos(angle) * overlap
            other.y -= math.sin(angle) * overlap

            nx = dx / distance
            ny = dy / distance
            tx = -ny 
            ty = nx 

            v1n = self.velx * nx + self.vel * ny
            v1t = self.velx * tx + self.vel * ty
            v2n = other.velx * nx + other.vel * ny
            v2t = other.velx * tx + other.vel * ty

            v1n_after = (v1n * (self.mass - other.mass) + 2 * other.mass * v2n) / (self.mass + other.mass)
            v2n_after = (v2n * (other.mass - self.mass) + 2 * self.mass * v1n) / (self.mass + other.mass)

            self.velx = v1n_after * nx + v1t * tx 
            self.vel = v1n_after * ny + v1t * ty 
            other.velx = v2n_after * nx + v2t * tx 
            other.vel = v2n_after * ny + v2t * ty 
        
    

ball_list=[]
for i in range(5):
    ball=Ball(800+5*i,100+i*25,10+8*i,5,2+i,1+2*i)
    ball_list.append(ball)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(60)

    display_surface.fill((0, 0, 0))
    for i, balls in enumerate(ball_list):
        balls.draw()
        balls.move()
        for j, other in enumerate(ball_list):
            if i != j:
                balls.checkcol(other)
    pygame.display.update()

pygame.quit()