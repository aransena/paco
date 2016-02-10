import paco
import random
import math
import matplotlib.pyplot as plt

num_cities = 100 # configure how many cities to populate the world with
world_x = 100 # set the max x,y dimensions for the world
world_y = 100
increment = 360.0/num_cities # calculate the increment required if we want to lay the cities out in a circle

aco = paco.ACO(num_cities,initial_pheromone=1,alpha=1,beta=3,epsilon=0.1,pheromone_deposit=2,evaporation_constant=0.6) # intialize the aco algorithm with our parameters
# see website for discussion of the above parameters

for i in range(0, num_cities):
    #aco.add_cities(paco.City(i, random.uniform(0,world_x), random.uniform(0,world_y))) # use this line for randomly distributed cities

    angle = i*increment # use this line and the next for cities distributed in a circle
    aco.add_cities(paco.City(i,math.sin(math.radians(angle)),math.cos(math.radians(angle)))) # populate the aco instance with the cities
    
shortest_path = aco.get_best_path(num_ants=3,num_steps=10) # run the aco algorithm and return the shortest path
print "Shortest route found: ", aco.shortest_path_len # print the shortest path length found in the aco

plt.figure(1)

plt.margins(0.1,0.1)

for i,c in enumerate(aco.cities): # output the cities to a plot
    if i == 0:
        plt.plot(c.x, c.y,'go') # the first city to be printed will be green
    else:
        plt.plot(c.x, c.y,'bo')
        
for i in xrange(0,len(shortest_path)-1): # plot connecting lines between each city visited in the order they are visited
    plt.plot([shortest_path[i].x,shortest_path[i+1].x],[shortest_path[i].y,shortest_path[i+1].y],'c-', linewidth=2.0,alpha=0.4)

plt.show()
