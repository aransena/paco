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
        for i in xrange(0,len(a.path)-1,2):
            curr_pher = self.pheromone[a.path[i].index][a.path[i+1].index]
            self.pheromone[a.path[i].index][a.path[i+1].index] = curr_pher + self.pheromone_deposit/a.path_length

        self.pheromone = self.pheromone*(1-self.evaporationConst)
#        self.pheromone = self.pheromone*(1-self.evaporationConst) + self.pheromone_deposit/path_len

    def get_pheromone(self,i,j):
        return self.pheromone[i][j]
