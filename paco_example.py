import paco
import random
import matplotlib.pyplot as plt

num_cities = 100
world_x = 100
world_y = 100

aco = paco.ACO(num_cities)

for i in range(0, num_cities):
    aco.add_cities(paco.City(i, random.uniform(0,world_x), random.uniform(0,world_y)))
    
shortest_path = aco.get_best_path(num_ants=10)
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
