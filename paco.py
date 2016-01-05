#!/usr/bin/env python
import numpy
import math
import ant
import city
import types
import random

from multiprocessing import Process, Queue

class ACO:
    def __init__(self,num_cities,initial_pheromone=1,alpha=1,beta=3,epsilon=0.01,pheromone_deposit=1,evaporation_constant=0.6):
        self.cities=[]
        self.shortest_paths=[]
        self.shortest_paths_lens=[]
        self.shortest_path_len=-1
        self.evaporationConst=evaporation_constant
        self.pheromone_deposit=pheromone_deposit
        self.pheromone=numpy.full((num_cities,num_cities),initial_pheromone)
        self.alpha=alpha
        self.beta=beta
        self.attractiveness=numpy.zeros((num_cities,num_cities))
        self.epsilon=epsilon
        self.routing_table=numpy.full((num_cities,num_cities),(1.00/(num_cities-1))) #initial even prob of any city


    def add_cities(self, city):
        if isinstance(city, list):
            self.cities.extend(city)
        else:
            self.cities.append(city)

    def calc_attraction(self):
        city_list=self.cities
        for i,c in enumerate(city_list):
            for j,d in enumerate(city_list):
                distance = self.calc_distance(c,d)
                if distance > 0:
                    self.attractiveness[i][j] = 1/distance
                else:
                    self.attractiveness[i][j] = 0

    def update_pheromone(self,a):
        for i in xrange(0,len(a.path)):
            try:
                curr_pher = self.pheromone[a.path[i].index][a.path[i+1].index]
                self.pheromone[a.path[i].index][a.path[i+1].index] = curr_pher + self.pheromone_deposit/a.path_length
            except:
                break

        self.pheromone = self.pheromone*(1-self.evaporationConst)
#        self.pheromone = self.pheromone*(1-self.evaporationConst) + self.pheromone_deposit/path_len

    def get_pheromone(self,i,j):
        return self.pheromone[i][j]

    def update_routing_table(self,a):
        for c in a.path:
            temp_cities = list(a.path)
            temp_cities.remove(c)
            for t_c in temp_cities:
                numerator = self.city_sum(c,t_c)
                denom = 0.00
                other_temp_cities = list(temp_cities)
                other_temp_cities.remove(t_c)
                for o_t_c in other_temp_cities:
                    denom = denom + self.city_sum(c,o_t_c)

                if denom>0:
                    self.routing_table[c.index][t_c.index]=numerator/denom
                else:
                    self.routing_table[c.index][t_c.index]=0
                                    
    def city_sum(self, city_x,city_y):
        calc = (math.pow(self.pheromone[city_x.index][city_y.index], self.alpha))*(math.pow(self.attractiveness[city_x.index][city_y.index],self.beta))
        return calc

    def get_best_path(self, num_ants=2, num_steps=3):      
        NUM_CITIES=len(self.cities)
        NUM_ANTS=num_ants
        NUM_STEPS=num_steps
        self.calc_attraction()
        ants=[]
        
        for i in xrange(0,NUM_ANTS):
            ants.append(ant.Ant(i,self))

        for step in xrange(0,NUM_STEPS):
            print "Step: ", step+1, " of ", NUM_STEPS
            path_lens=[]
            paths=[]
            argu = self
            procs = []

            q = Queue()

            for a in ants:
                p = Process(target=self.mp_tour,args=(a,q,))
                procs.append(p)
                p.start()

            for p in procs:
                p.join()

            ants = []
            while q.empty()==False:
                ants.append(q.get())
            
            for a in ants:
                path_len = a.calc_path_length()
                path_lens.append(path_len)
                paths.append(a.path)

            best_path_len = min(path_lens)
            best_path = paths[path_lens.index(best_path_len)]
            self.shortest_paths.append(best_path)
            self.shortest_paths_lens.append(best_path_len)
            for a in ants:
                self.update_pheromone(a)
                self.update_routing_table(a)

        output_index = self.shortest_paths_lens.index(min(self.shortest_paths_lens))
        output_path = self.shortest_paths[output_index]
        self.shortest_path_len = self.shortest_paths_lens[output_index]
        self.shortest_paths=[]
        self.shortest_paths_lens=[]

        return output_path

    def calc_distance(self,city1,city2):
        distance =  math.sqrt(math.pow((city1.x-city2.x),2)+math.pow((city1.y-city2.y),2))
        return distance

    def mp_tour(self,ant,q):
        ant.reset_ant(self)
        while(ant.unvisited):
            if random.random()<0:#world.epsilon:
                next_city = ant.unvisited.pop(random.randint(0,len(ant.unvisited)-1))
                ant.path.append(next_city)
                ant.currCity=next_city

            else:
                for c in ant.unvisited:
#                    self.transition_probs.append(self.calc_transition_prob(world,c))
                    ant.transition_probs.append(ant.get_transition_prob(self,c))
                
                ant.transition_probs= ant.transition_probs/sum(ant.transition_probs)
                selection = numpy.random.choice(ant.unvisited,1,p=ant.transition_probs)
                next_city = selection[0]
                ant.path.append(next_city)
                ant.currCity=next_city
                ant.unvisited.pop(ant.unvisited.index(next_city))
            ant.transition_probs=[]
        q.put(ant)

class City:
    def __init__(self,i=0, x_cord=0, y_cord=0,prob=0):
        self.index = i
        self.x = x_cord
        self.y = y_cord
           
        
