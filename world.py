#!/usr/bin/env python

class World:
    def __init__(self):
        self.cities=[]
        self.evaporationConst=0.1
        self.dist_weight=0.1

    def add_cities(self, city):
        self.cities.append(city)

    def set_evaporation(self, evap):
        self.evaporationConst=evap

    def set_dist_weight(self, dist):
        self.dist_weight=dist
