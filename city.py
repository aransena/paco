#!/usr/bin/env python
import numpy

class City:
    def __init__(self,i, x_cord, y_cord,prob,objs):
        self.index = i
        self.x = x_cord
        self.y = y_cord
        self.objects = []
        self.objects.extend(objs)
        self.probability = prob
        
    def add_objects(hidden_objects):
        self.objects.append(hidden_objects)
    
        
        
