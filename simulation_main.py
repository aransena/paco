#!/usr/bin/env python
import city
import world
import random
import math
import ant
from scipy.stats import norm
import numpy

random.seed(2)
numpy.random.seed(2)
NUM_CITIES=30
NUM_ANTS=100
NUM_STEPS=10
WORLD_X = 100
WORLD_Y = 100
NUM_OBJECTS=10

objects = range(0,NUM_OBJECTS)

locations = world.World(NUM_CITIES,init_pheromone=1,a=1,b=3,ep=0.1,pheromone_deposit=1,evap_const=0.5)
prob_shifted_locations = world.World(NUM_CITIES,init_pheromone=1,a=1,b=3,ep=0.1,pheromone_deposit=1,evap_const=0.5)


mode = 0 #Mode 0: Uninform random Distribution, Mode 1: Circle

####setup world####
if mode==1:
    increment = 360.0/NUM_CITIES

x = numpy.linspace(0,10,NUM_CITIES)
y = norm.pdf(x,loc=5,scale=1)
prob_distribution= y
#print "probs: ", prob_distribution

for i in range(0,NUM_CITIES):

    #prob = random.random()
    prob = prob_distribution[i]
    
    if mode == 0:
        locations.add_cities(city.City(i,random.uniform(0,WORLD_X),random.uniform(0,WORLD_Y),prob,objs=[]))
        
    elif mode == 1:
        angle = i*increment
        locations.add_cities(city.City(i,math.sin(math.radians(angle)),math.cos(math.radians(angle)),prob,objs=[]))

for i, c in enumerate(locations.cities):
    if i==0:
        prob_shifted_locations.add_cities(city.City(i, (c.x), (c.y),1,objs=[]))
    else:
        prob_shifted_locations.add_cities(city.City(i, (c.x)/c.probability, (c.y)/c.probability,1,objs=[]))

locations.calc_attraction() # revisit - inefficient
prob_shifted_locations.calc_attraction()

ants=[]
p_ants=[]
for i in range(0,NUM_ANTS):
    ants.append(ant.Ant(i,locations))
    p_ants.append(ant.Ant(i,prob_shifted_locations))
    
for step in range(0,NUM_STEPS):
    #locations.ep=max(1/(step+1.00),0.5)
    #locations.evap_const=max((NUM_STEPS-step)/float(NUM_STEPS),0.5)
    i = 0
    for a in ants:
        a.tour(locations)
        path_len = a.calc_path_length()
        if i == 0 and step == 0:
            i=1
            best_path_len = path_len
            best_path = list(a.path)

            print "best path: ", best_path_len, " step: ", step

        elif path_len < best_path_len:
            best_path_len = path_len
            best_path = list(a.path)
            print "best path: ", best_path_len, " step: ", step

    for a in ants:
        locations.update_pheromone(a)
        locations.update_routing_table(a)
    
        #locations.update_pheromone(best_path)
for step in range(0,NUM_STEPS):
    prob_shifted_locations.ep=max(1/(step+1),0.1)
    i = 0
    for a in p_ants:
        a.tour(prob_shifted_locations)
        path_len = a.calc_path_length()
        if i == 0 and step == 0:
            i = 1
            best_p_path_len = path_len
            best_p_path = a.path

        elif path_len < best_p_path_len:
            best_p_path_len = path_len
            best_p_path = a.path
            print "best p_path: ", best_p_path_len, " step: ", step

    for a in p_ants:
        prob_shifted_locations.update_pheromone(a)

        prob_shifted_locations.update_routing_table(a)
        #locations.update_pheromone(best_path)

####Visualize world####
import matplotlib.pyplot as plt
plt.figure(1)
plt.autoscale(tight=False)
plt.subplot(121)
plt.margins(0.1,0.1)
for i,c in enumerate(locations.cities):
    if i == 0:
        plt.plot(c.x, c.y,'go')
    elif i == len(locations.cities)-1:
        plt.plot(c.x, c.y,'ro')
    else:
        plt.plot(c.x, c.y,'bo')

    for i in xrange(0,len(best_p_path)-1):
        #for c in best_path:
        plt.plot([locations.cities[best_p_path[i].index].x,locations.cities[best_p_path[i+1].index].x],[locations.cities[best_p_path[i].index].y,locations.cities[best_p_path[i+1].index].y],'c-', linewidth=2.0,alpha=0.3)

plt.subplot(122)
plt.margins(.1,.1)
for i in xrange(0,len(best_path)-1):
    plt.plot([best_path[i].x,best_path[i+1].x],[best_path[i].y,best_path[i+1].y],'c-', linewidth=2.0,alpha=0.4)

plt.figure(2)
plt.subplot(121)
plt.margins(0.1,0.1)
for i,c in enumerate(prob_shifted_locations.cities):
    if i == 0:
        plt.plot(c.x, c.y,'go')
    elif i == len(prob_shifted_locations.cities)-1:
        plt.plot(c.x, c.y,'ro')
    else:
        plt.plot(c.x, c.y,'bo')

plt.subplot(122)
plt.margins(0.1,.1)
for i in xrange(0,len(best_p_path)-1):
#for c in best_path:
    plt.plot([best_p_path[i].x,best_p_path[i+1].x],[best_p_path[i].y,best_p_path[i+1].y],'c-', linewidth=2.0)


plt.figure(3)
max_pher = numpy.max(locations.pheromone)
plt.subplot(121)
plt.margins(0.1,0.1)
for i in range(0,NUM_CITIES):
    for j in range(0,NUM_CITIES):
        x = 0
        plt.plot([locations.cities[i].x,locations.cities[j].x],[locations.cities[i].y,locations.cities[j].y], 'r-', alpha=locations.get_pheromone(i,j)/max_pher)
        
plt.subplot(122)
plt.margins(0.1,0.1)
for i in range(0,NUM_CITIES):
    for j in range(0,NUM_CITIES):
        plt.plot([prob_shifted_locations.cities[i].x,prob_shifted_locations.cities[j].x],[prob_shifted_locations.cities[i].y,prob_shifted_locations.cities[j].y], 'r-', alpha=locations.get_pheromone(i,j)/max_pher)

plt.show()
    
