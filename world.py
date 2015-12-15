#!/usr/bin/env python
import numpy
import math

class World:
    def __init__(self,num_cities,init_pheromone=0.5,a=0.2,b=0.2,ep=0.01):
        self.cities=[]
        self.evaporationConst=0.1
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

            
