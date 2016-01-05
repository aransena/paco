import paco
import random
import math
import matplotlib.pyplot as plt

num_cities = 100
world_x = 100
world_y = 100
increment = 360.0/num_cities

aco = paco.ACO(num_cities,initial_pheromone=1,alpha=1,beta=3,epsilon=0.1,pheromone_deposit=2,evaporation_constant=0.6)

for i in range(0, num_cities):
    #aco.add_cities(paco.City(i, random.uniform(0,world_x), random.uniform(0,world_y)))
    angle = i*increment
    aco.add_cities(paco.City(i,math.sin(math.radians(angle)),math.cos(math.radians(angle))))
    
shortest_path = aco.get_best_path(num_ants=3,num_steps=10)
print "Shortest route found: ", aco.shortest_path_len

plt.figure(1)
plt.margins(0.1,0.1)

for i,c in enumerate(aco.cities):
    if i == 0:
        plt.plot(c.x, c.y,'go')
    else:
        plt.plot(c.x, c.y,'bo')
        
for i in xrange(0,len(shortest_path)-1):
    plt.plot([shortest_path[i].x,shortest_path[i+1].x],[shortest_path[i].y,shortest_path[i+1].y],'c-', linewidth=2.0,alpha=0.4)


plt.show()
