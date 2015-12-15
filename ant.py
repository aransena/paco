#!/usr/bin/env python
import world
import math
import city
import random
import numpy

class Ant:
    def __init__(self,i,world):
        self.index = i
        self.path_length = 0
        self.currCity=world.cities[0]
        self.path=[]
        self.path.append(world.cities[0])
        self.unvisited=[]
        self.unvisited.extend(world.cities[1:])
        self.transition_probs=[]
        
    def calc_transition_prob(self,world,city_y):
        numerator = self.city_sum(world,self.currCity,city_y)
        sum = 0
        for c in self.unvisited:
            sum = sum + self.city_sum(world,self.currCity,c)

        return numerator/sum

    def city_sum(self, world, city_x,city_y):
        return (math.pow(world.pheromone[city_x.index][city_y.index], world.alpha))*(math.pow(world.attractiveness[city_x.index][city_y.index],world.beta))

    def tour(self,world):
        while(self.unvisited):
            if random.random()<world.epsilon:
                next_city = self.unvisited.pop(random.randint(0,len(self.unvisited)-1))
                self.path.append(next_city)
                self.currCity=next_city

            else:
                for c in self.unvisited:
                    self.transition_probs.append(self.calc_transition_prob(world,c))
                selection = numpy.random.choice(self.unvisited,1,p=self.transition_probs)
                next_city = selection[0]
                self.path.append(next_city)
                self.currCity=next_city
                self.unvisited.pop(self.unvisited.index(next_city))
            self.transition_probs=[]

    def calc_path_length(self):
        sum_dist=0
        for i in xrange(0,len(self.path),2):
            distance =  math.sqrt(math.pow((self.path[i].x-self.path[i+1].x),2)+math.pow((self.path[i].y-self.path[i+1].y),2))            
            sum_dist=sum_dist+distance
        self.path_length = sum_dist
        return sum_dist
            
