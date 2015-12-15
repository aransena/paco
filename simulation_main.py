#!/usr/bin/env python
import city
import world
import random
import math
import ant

random.seed(2)

NUM_CITIES=10
NUM_ANTS=10
NUM_STEPS=1000
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
p_ants=[]
for i in range(0,NUM_ANTS):
    ants.append(ant.Ant(i,locations))
    p_ants.append(ant.Ant(i,prob_shifted_locations))
    
for step in range(0,NUM_STEPS):
    for i,a in enumerate(ants):
        a.tour(locations)
        path_len = a.calc_path_length()
        if i == 0 and step == 0:
            best_path_len = path_len
            best_path = a.path
        elif path_len < best_path_len:
            best_path_len = path_len
            best_path = a.path
            print "best path: ", best_path_len

    for a in ants:
        locations.update_pheromone(a)
        #locations.update_pheromone(best_path)

for step in range(0,NUM_STEPS):
    for i,a in enumerate(p_ants):
        a.tour(prob_shifted_locations)
        path_len = a.calc_path_length()
        if i == 0 and step == 0:
            best_p_path_len = path_len
            best_p_path = a.path
        elif path_len < best_path_len:
            best_p_path_len = path_len
            best_p_path = a.path
            print "best p_path: ", best_p_path_len

    for a in p_ants:
        prob_shifted_locations.update_pheromone(a)
        #locations.update_pheromone(best_path)
            
    

####Visualize world####
import matplotlib.pyplot as plt
plt.figure()
plt.autoscale(tight=False)

plt.subplot(411)
plt.margins(0.1,0.1)
for i,c in enumerate(locations.cities):
    if i == 0:
        plt.plot(c.x, c.y,'go')
    elif i == len(locations.cities)-1:
        plt.plot(c.x, c.y,'ro')
    else:
        plt.plot(c.x, c.y,'bo')

plt.subplot(412)
plt.margins(0.1,0.1)
for i in xrange(0,len(best_path)-1):
#for c in best_path:
    plt.plot([best_path[i].x,best_path[i+1].x],[best_path[i].y,best_path[i+1].y],'k-', linewidth=2.0)
    
plt.subplot(413)
plt.margins(0.1,0.1)
for i,c in enumerate(prob_shifted_locations.cities):
    if i == 0:
        plt.plot(c.x, c.y,'go')
    elif i == len(prob_shifted_locations.cities)-1:
        plt.plot(c.x, c.y,'ro')
    else:
        plt.plot(c.x, c.y,'bo')

plt.subplot(414)
plt.margins(0.1,0.1)
for i in xrange(0,len(best_p_path)-1):
#for c in best_path:
    plt.plot([best_p_path[i].x,best_p_path[i+1].x],[best_p_path[i].y,best_p_path[i+1].y],'k-', linewidth=2.0)


        
plt.show()
    
