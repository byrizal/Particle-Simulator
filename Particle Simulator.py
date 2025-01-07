import pygame
from random import randint
pygame.init()

#Screen Size
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption ('Particle Interaction')



class Particles:
    def __init__(self, position, radius, color, displacement_x=0, displacement_y=0, acceleration_y=0.1, elastic_eff=0.8):
        self.position = list(position)
        self.radius = radius
        self.color = color
        self.displacement_x = displacement_x
        self.displacement_y = displacement_y
        self.acceleration_y = acceleration_y
        self.elastic_eff = elastic_eff

    def update(self, time_tick, screen_width, screen_height):
        
        #Gravitational Acceleration
        self.displacement_y = self.displacement_y + (self.acceleration_y * time_tick)

        #Change Position
        self.position[0] += self.displacement_x
        self.position[1] += self.displacement_y

        #Checks Edge
        if self.position[0] - self.radius < 0:
            self.position[0] = self.radius
            self.displacement_x = -self.displacement_x * self.elastic_eff
        if self.position[0] + self.radius > screen_width:
            self.position[0] = screen_width - self.radius
            self.displacement_x = -self.displacement_x * self.elastic_eff
        if self.position[1] - self.radius < 0:
            self.position[1] = self.radius
            self.displacement_y = -self.displacement_y * self.elastic_eff
        if self.position[1] + self.radius > screen_height:
            self.position[1] = screen_height - self.radius
            self.displacement_y = -self.displacement_y * self.elastic_eff
        
    
    #Checks Collision
    def collision(self, other):
        collision_x = abs(other.position[0] - self.position[0])
        collision_y = abs(other.position[1] - self.position[1])
        
        # Check if particles overlap
        if collision_x < self.radius + other.radius and collision_y < self.radius + other.radius:
            overlap_x = (self.radius + other.radius) - collision_x
            overlap_y = (self.radius + other.radius) - collision_y
            
            # Push particles apart based on the axis of overlap
            if collision_x > collision_y:
                if self.position[0] > other.position[0]:
                    self.position[0] += overlap_x / 2
                    other.position[0] -= overlap_x / 2
                else:
                    self.position[0] -= overlap_x / 2
                    other.position[0] += overlap_x / 2
                self.displacement_x = -self.displacement_x * self.elastic_eff
                other.displacement_x = -other.displacement_x * other.elastic_eff
            else:
                if self.position[1] > other.position[1]:
                    self.position[1] += overlap_y / 2
                    other.position[1] -= overlap_y / 2
                else:
                    self.position[1] -= overlap_y / 2
                    other.position[1] += overlap_y / 2
                self.displacement_y = -self.displacement_y * self.elastic_eff
                other.displacement_y = -other.displacement_y * other.elastic_eff
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius)
             



particle = [] #Contains all Particles
time_tick = 0.01 #Rate of Time

#Spawns Particles
for _ in range(50):
    random_position = [randint(50, SCREEN_WIDTH - 50), randint(50, SCREEN_HEIGHT - 50)]
    random_color = (randint(0, 255), randint(0, 255), randint(0, 255))
    new_particle = Particles(position=random_position, radius=10, color=random_color, displacement_x=randint(1, 3), displacement_y=randint(1, 3))
    particle.append(new_particle)


RUN = True
while RUN == True:

    #Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

    # Clear screen
    screen.fill((0, 0, 0))

    #Update and Draw all Particles
    for particle_instance in particle:
        particle_instance.update(time_tick, SCREEN_WIDTH, SCREEN_HEIGHT)
        particle_instance.draw(screen)

    for i, particle_instance in enumerate(particle):
        for j in range(i + 1, len(particle)):
            particle_instance.collision(particle[j])

    #Refresh
    pygame.display.update()

pygame.quit()