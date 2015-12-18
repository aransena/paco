#!/usr/bin/env python
import numpy
import math
import ant
import city

class World:
    def __init__(self,num_cities,init_pheromone=1,a=1,b=3,ep=0.01,pheromone_deposit=1,evap_const=0.6,num_objs=1):
        self.cities=[]
        self.num_objects=num_objs
        self.shortest_paths=[]
        self.shortest_paths_lens=[]
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

    def get_best_path(self, params):
        NUM_CITIES=params[0]
        NUM_ANTS=params[1]
        NUM_STEPS=params[2]

        ants=[]
        
        for i in xrange(0,NUM_ANTS):
            ants.append(ant.Ant(i,self))

        for step in xrange(0,NUM_STEPS):
            path_lens=[]
            paths=[]

            for a in ants:
                a.tour(self)
                path_len = a.calc_path_length()
                path_lens.append(path_len)
                paths.append(a.path)

            best_path_len = min(path_lens)
            best_path = paths[path_lens.index(best_path_len)]
            #print "step best path: ", best_path_len, " step: ", step
            self.shortest_paths.append(best_path)
            self.shortest_paths_lens.append(best_path_len)
            for a in ants:
                self.update_pheromone(a)
                self.update_routing_table(a)

        output_index = self.shortest_paths_lens.index(min(self.shortest_paths_lens))
        output_path = self.shortest_paths[output_index]
        print "best overall path: ", self.shortest_paths_lens[output_index]
        self.shortest_paths=[]
        self.shortest_paths_lens=[]
        return output_path

    def add_objects(self,objects):
        while objects:
            for c in self.cities:
                if numpy.random.random() < c.probability:
                    if objects and len(c.objects)==0:
                        c.objects.append(objects.pop())

                    else:
                        break

        for i,c in enumerate(self.cities):
            if len(c.objects)>0:
                print c.index, c.objects

    def get_time_to_find_objects(self, path):
        objs_found=0
        dist_travelled=0
        prev_city=self.cities[0]
        for c in path[1:]:
            if len(self.cities[c.index].objects)>0:
                objs_found+=1
            dist_travelled += self.calc_distance(self.cities[prev_city.index],self.cities[c.index])

            if objs_found == self.num_objects:
                return dist_travelled

        return -1

    def calc_distance(self,city1,city2):
        distance =  math.sqrt(math.pow((city1.x-city2.x),2)+math.pow((city1.y-city2.y),2))
        return distance
