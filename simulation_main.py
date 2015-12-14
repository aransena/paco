#!/usr/bin/env python
import city
import world

dublin = city.City(0,10,10)
london = city.City(1,30,30)
italy= city.City(2,14,14)

earth = world.World()

earth.add_cities(dublin)
earth.add_cities(london)
earth.add_cities(italy)

import matplotlib.pyplot as plt

print "CITIES: ", earth.cities
print "DUBLIN x: ", dublin.x

plt.figure()
for c in earth.cities:
    print c
    plt.plot(c.x, c.y,'ro')
plt.show()
    
