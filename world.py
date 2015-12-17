#!/usr/bin/env python
import numpy
import math
import ant

class World:
    def __init__(self,num_cities,init_pheromone=1,a=1,b=3,ep=0.01,pheromone_deposit=1,evap_const=0.6):
        self.cities=[]
        self.evaporationConst=evap_const
        self.pheromone_deposit=1
        self.dist_weight=0.1
        self.pheromone=numpy.zeros((num_cities,num_cities))
        self.pheromone[:]=init_pheromone
        self.alpha=a
        self.beta=b
        self.attractiveness=numpy.zeros((num_cities,num_cities))
        self.epsilon=ep
        self.routing_table=numpy.zeros((num_cities,num_cities))
        self.routing_table[:]=1.00/(num_cities-1) #initial even prob of any city

    def add_cities(self, city):
        self.cities.append(city)

    def calc_attraction(self):
        city_list=self.cities
        for i,c in enumerate(city_list):
            for j,d in enumerate(city_list):
                distance =  math.sqrt(math.pow((c.x-d.x),2)+math.pow((c.y-d.y),2))
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
