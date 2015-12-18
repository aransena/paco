#!/usr/bin/env python
import city
import world
import random
import math
import ant
from scipy.stats import norm,pareto,lognorm
import numpy
import sys
import datetime
import time
import bisect

ts = time.time()
dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
Root = "Result_Images/"

plot=False

mode = 1 #Mode 0: Uninform random Distribution, Mode 1: Circle

SEED_NUM=2
random.seed(2)
numpy.random.seed(2)
NUM_CITIES=10
NUM_ANTS=max(int(NUM_CITIES/5),2)
NUM_STEPS=10
WORLD_X = 100
WORLD_Y = 100
NUM_OBJECTS=max(int(NUM_CITIES/3),1)

i_pher=1
alpha=1
beta=5
exp=0.1
pher_dep=1
evap_c=0.3

params=[]
params.append(NUM_CITIES)
params.append(NUM_ANTS)
params.append(NUM_STEPS)
params.append(NUM_OBJECTS)
params.append(SEED_NUM)
params.append(i_pher)
params.append(alpha)
params.append(beta)
params.append(exp)
params.append(pher_dep)
params.append(evap_c)


objects = range(0,NUM_OBJECTS)

locations = world.World(NUM_CITIES,init_pheromone=i_pher,a=alpha,b=beta,ep=exp,pheromone_deposit=pher_dep,evap_const=evap_c,num_objs=NUM_OBJECTS)
prob_shifted_locations = world.World(NUM_CITIES,init_pheromone=i_pher,a=alpha,b=beta,ep=exp,pheromone_deposit=pher_dep,evap_const=evap_c)

####setup world####
if mode==1:
    increment = 360.0/NUM_CITIES

xx = numpy.linspace(0,10,NUM_CITIES)
y1 = norm.pdf(xx,loc=2,scale=1)
y2 = norm.pdf(xx,loc=8,scale=1)
yy = [a + b for a, b in zip(y1, y2)]
#print yy
yy = yy/(sum(yy))

#y = pareto.pdf(xx,1)
#yy = lognorm.pdf(xx,50)

prob_distribution= yy
min_prob = (min(filter(None,prob_distribution))/10)
for i in xrange(0,len(prob_distribution)):
    if prob_distribution[i]==0:
        prob_distribution[i]=min_prob
        
#print "probs: ", prob_distribution

for i in range(0,NUM_CITIES):
    #prob = random.random()
    prob = prob_distribution[i]
    
    if mode == 0:
        locations.add_cities(city.City(i,random.uniform(0,WORLD_X),random.uniform(0,WORLD_Y),prob))
        
    elif mode == 1:
        angle = i*increment
        locations.add_cities(city.City(i,math.sin(math.radians(angle)),math.cos(math.radians(angle)),prob))
            
for i, c in enumerate(locations.cities):
    if i==0:
        prob_shifted_locations.add_cities(city.City(i, (c.x), (c.y),1))
    else:
        
        prob_shifted_locations.add_cities(city.City(i, (c.x)/c.probability, (c.y)/c.probability,1))

max_likelihood=[0]
for c in locations.cities[1:]:
    bisect.insort(max_likelihood,c.probability)

temp_c = list(locations.cities)

max_likelihood_path=[]
for m_l in max_likelihood:
    for i,c in enumerate(temp_c):
        if c.probability==m_l:
            max_likelihood_path.append(temp_c.pop(i))
max_likelihood_path=list(reversed(max_likelihood_path))
print "ML: ",len(max_likelihood_path)
locations.add_objects(objects)

locations.calc_attraction() # revisit - inefficient
prob_shifted_locations.calc_attraction()
start=time.time()
best_path = locations.get_best_path(params)
best_p_path = prob_shifted_locations.get_best_path(params)
delT=time.time()-start

time_to_find_pshifted = locations.get_time_to_find_objects(best_p_path)
time_to_find_shortest = locations.get_time_to_find_objects(best_path)

print "Shortest path: ", time_to_find_shortest, " PShifted: ", time_to_find_pshifted, " Improvement: ", (time_to_find_pshifted-time_to_find_shortest)/time_to_find_shortest, " run time: ", delT


f = open('results.txt','a')
str_wr = dt + ", "
str_wr += str(time_to_find_shortest)+', '+str(time_to_find_pshifted)+', '
for p in params:
    str_wr+=str(p)+', '
str_wr+=str(delT)
str_wr+="\n"
f.write(str_wr)

##################################################################################
####Visualize world####


import matplotlib.pyplot as plt
plt.figure(1)
plt.autoscale(tight=False)
plt.subplot(131)
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

plt.title('probability shifted route')

plt.subplot(132)
plt.margins(.1,.1)
for i,c in enumerate(locations.cities):
    if i == 0:
        plt.plot(c.x, c.y,'go')
    elif i == len(locations.cities)-1:
        plt.plot(c.x, c.y,'ro')
    else:
        plt.plot(c.x, c.y,'bo')

for i in xrange(0,len(best_path)-1):
    plt.plot([best_path[i].x,best_path[i+1].x],[best_path[i].y,best_path[i+1].y],'c-', linewidth=2.0,alpha=0.4)

plt.title('shortest route')

plt.subplot(133)
plt.margins(.1,.1)
for i,c in enumerate(locations.cities):
    if i == 0:
        plt.plot(c.x, c.y,'go')
    elif i == len(locations.cities)-1:
        plt.plot(c.x, c.y,'ro')
    else:
        plt.plot(c.x, c.y,'bo')

for i in xrange(0,len(max_likelihood_path)-1):
    plt.plot([max_likelihood_path[i].x,max_likelihood_path[i+1].x],[max_likelihood_path[i].y,max_likelihood_path[i+1].y],'c-', linewidth=2.0,alpha=0.4)

plt.title('max likelihood route')

plt.savefig(Root+"optimal_paths "+dt+".png")

plt.figure(2)
plt.margins(0.1,0.1)
for i,c in enumerate(prob_shifted_locations.cities):
    if i == 0:
        plt.plot(c.x, c.y,'go')
    elif i == len(prob_shifted_locations.cities)-1:
        plt.plot(c.x, c.y,'ro')
    else:
        plt.plot(c.x, c.y,'bo')

for i in xrange(0,len(best_p_path)-1):
#for c in best_path:
    plt.plot([best_p_path[i].x,best_p_path[i+1].x],[best_p_path[i].y,best_p_path[i+1].y],'c-', linewidth=2.0)

plt.title('probability shifted route')

plt.savefig(Root+"prob_shifted "+dt+".png")

plt.figure(3)
max_pher = numpy.max(locations.pheromone)
plt.subplot(121)
plt.margins(0.1,0.1)
for i in range(0,NUM_CITIES):
    for j in range(0,NUM_CITIES):
        x = 0
        plt.plot([locations.cities[i].x,locations.cities[j].x],[locations.cities[i].y,locations.cities[j].y], 'r-', alpha=locations.get_pheromone(i,j)/max_pher)

plt.title('probability shifted')
        
plt.subplot(122)
plt.margins(0.1,0.1)
for i in range(0,NUM_CITIES):
    for j in range(0,NUM_CITIES):
        plt.plot([prob_shifted_locations.cities[i].x,prob_shifted_locations.cities[j].x],[prob_shifted_locations.cities[i].y,prob_shifted_locations.cities[j].y], 'r-', alpha=locations.get_pheromone(i,j)/max_pher)

plt.title('shortest')

plt.savefig(Root+"pheromone "+dt+".png")

plt.figure(4)
plt.plot(xx,yy)
plt.title('underlying distribution')
plt.savefig(Root+"distribution "+dt+".png")

if plot==True:
   #sys.exit("Set to not plot")
    plt.show()
    
