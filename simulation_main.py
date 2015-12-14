#!/usr/bin/env python
import city
import world
from random import randint
import math

NUM_CITIES=100
WORLD_X = 100
WORLD_Y = 100

earth = world.World()

mode = 0 #Mode 0: Uninform random Distribution, Mode 1: Circle

if mode==1:
    increment = 360.0/NUM_CITIES

for i in range(0,NUM_CITIES):
    if mode == 0:
        earth.add_cities(city.City(i,randint(0,WORLD_X),randint(0,WORLD_Y)))
        
    elif mode == 1:
        angle = i*increment
        earth.add_cities(city.City(i,math.sin(math.radians(angle)),math.cos(math.radians(angle))))


# Visualize world
import matplotlib.pyplot as plt
plt.figure()
plt.autoscale(tight=False)
plt.margins(0.1,0.1)
for c in earth.cities:
    plt.plot(c.x, c.y,'ro')
plt.show()
    
