#!/usr/bin/env python
import city
import world
import random
import math
import ant

random.seed(2)

NUM_CITIES=10
NUM_ANTS=10
WORLD_X = 100
WORLD_Y = 100


locations = world.World(NUM_CITIES)
prob_shifted_locations = world.World(NUM_CITIES, init_pheromone=0.3,a=0.5,b=0.4)

mode = 1 #Mode 0: Uninform random Distribution, Mode 1: Circle

####setup world####
if mode==1:
    increment = 360.0/NUM_CITIES

for i in range(0,NUM_CITIES):

    prob = random.random()
    
    if mode == 0:
        locations.add_cities(city.City(i,random.uniform(0,WORLD_X),random.uniform(0,WORLD_Y),prob))
        
    elif mode == 1:
        angle = i*increment
        locations.add_cities(city.City(i,math.sin(math.radians(angle)),math.cos(math.radians(angle)),prob))

for i, c in enumerate(locations.cities):
    prob_shifted_locations.add_cities(city.City(i, (c.x)/c.probability, (c.y)/c.probability,1))

locations.calc_attraction() # revisit - inefficient
prob_shifted_locations.calc_attraction()

ants=[]
for i in range(0,NUM_ANTS):
    ants.append(ant.Ant(i,locations))

for a in ants:
    a.tour(locations)
    print a.calc_path_length()

####Visualize world####
import matplotlib.pyplot as plt
plt.figure()
plt.autoscale(tight=False)

plt.subplot(211)
plt.margins(0.1,0.1)
for i,c in enumerate(locations.cities):
    if i == 0:
        plt.plot(c.x, c.y,'go')
    elif i == len(locations.cities)-1:
        plt.plot(c.x, c.y,'ro')
    else:
        plt.plot(c.x, c.y,'bo')
plt.subplot(212)
plt.margins(0.1,0.1)
for i,c in enumerate(prob_shifted_locations.cities):
    if i == 0:
        plt.plot(c.x, c.y,'go')
    elif i == len(prob_shifted_locations.cities)-1:
        plt.plot(c.x, c.y,'ro')
    else:
        plt.plot(c.x, c.y,'bo')
                       
plt.show()
    
