#!/usr/bin/env python
import city
import world
import random
import math
import ant
from scipy.stats import norm,pareto,lognorm
import numpy

random.seed(2)
numpy.random.seed(2)
NUM_CITIES=20
NUM_ANTS=max(int(NUM_CITIES/5),2)
NUM_STEPS=10
WORLD_X = 100
WORLD_Y = 100
NUM_OBJECTS=10

params=[]
params.append(NUM_CITIES)
params.append(NUM_ANTS)
params.append(NUM_STEPS)

objects = range(0,NUM_OBJECTS)

locations = world.World(NUM_CITIES,init_pheromone=1,a=1,b=5,ep=0.1,pheromone_deposit=1,evap_const=0.3)
prob_shifted_locations = world.World(NUM_CITIES,init_pheromone=1,a=1,b=5,ep=0.1,pheromone_deposit=1,evap_const=0.3)


mode = 1 #Mode 0: Uninform random Distribution, Mode 1: Circle

####setup world####
if mode==1:
    increment = 360.0/NUM_CITIES

xx = numpy.linspace(0,10,NUM_CITIES)
y1 = norm.pdf(xx,loc=5,scale=1)
y2 = norm.pdf(xx,loc=10,scale=1)
yy = [a + b for a, b in zip(y1, y2)]

#y = pareto.pdf(x,1)
#y = lognorm.pdf(x,50)

prob_distribution= yy
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

best_path = locations.get_best_path(params)
best_p_path = prob_shifted_locations.get_best_path(params)


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

plt.figure(4)
plt.plot(xx,yy)
plt.show()
    
