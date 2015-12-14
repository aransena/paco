#!/usr/bin/env python
import city
import world
import random
import math

random.seed(1)

NUM_CITIES=10
WORLD_X = 100
WORLD_Y = 100

earth = world.World()
bizarro = world.World()

mode = 1 #Mode 0: Uninform random Distribution, Mode 1: Circle

if mode==1:
    increment = 360.0/NUM_CITIES

for i in range(0,NUM_CITIES):

    prob = random.random()
    
    if mode == 0:
        earth.add_cities(city.City(i,random.uniform(0,WORLD_X),random.uniform(0,WORLD_Y),prob))
        
    elif mode == 1:
        angle = i*increment
        earth.add_cities(city.City(i,math.sin(math.radians(angle)),math.cos(math.radians(angle)),prob))

for i, c in enumerate(earth.cities):
    bizarro.add_cities(city.City(i, (c.x)/c.probability, (c.y)/c.probability,1))
            
        

# Visualize world

import matplotlib.pyplot as plt
plt.figure()
plt.autoscale(tight=False)

plt.subplot(211)
plt.margins(0.1,0.1)
for i,c in enumerate(earth.cities):
    if i == 0:
        plt.plot(c.x, c.y,'go')
    elif i == len(earth.cities)-1:
        plt.plot(c.x, c.y,'ro')
    else:
        plt.plot(c.x, c.y,'bo')
plt.subplot(212)
plt.margins(0.1,0.1)
for i,c in enumerate(bizarro.cities):
    if i == 0:
        plt.plot(c.x, c.y,'go')
    elif i == len(earth.cities)-1:
        plt.plot(c.x, c.y,'ro')
    else:
        plt.plot(c.x, c.y,'bo')
                       
plt.show()
    
