# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 19:31:48 2019

@author: hsauro
"""

import math
import numpy
import pylab
import random

numpy.random.seed (1234)
# Generate some synthetic data
dx=[]
dy=[]

theta = [20, 6, 0.4]
for x in numpy.arange (0, 40, 0.5):
    dx.append (x)
    dy.append (numpy.random.normal(theta[0]+theta[1]*math.sin(2.*math.pi/24.*x+theta[2]), 2))

pylab.plot (dx, dy)
pylab.show()
   
# Fit this Model to the data
def model (x,theta):
   return theta[0] + theta[1]*math.sin((2.0*math.pi/24.0)*x + theta[2])

# Chi Squared
def chi2(dx, dy, theta):
   s = 0.0
   for i in range(len(dx)):
      s += (model(dx[i], theta) - dy[i])**2
   return s/len(dx)

# Likelihood function
def P(dx, dy, theta):
   return math.exp (-chi2(dx, dy, theta))

# Initial guess for model parameters
theta1 = []; theta2 = []; theta3 = []
theta_current = [0.,0.,0.]
theta_proposed = [0.,0.,0.]
P_current = P(dx, dy, theta_current)
chain = []
for i in range(10000):
   theta_proposed[0]  = theta[0] + 0.1*numpy.random.randn()
   theta_proposed[1]  = theta[1] + 0.1*numpy.random.randn()
   theta_proposed[2]  = theta[2] + 0.1*numpy.random.randn()

   P_proposed = P (dx, dy, theta_proposed)
   ratio = min (1, P_proposed/P_current)
   
   r = numpy.random.rand()
   if ratio > r:
      theta_current = theta_proposed
      P_current = P_proposed
   if i >= 5000: # save chain only after burnin
      chain.append(theta_current)
      theta1.append (theta_current[0])
      theta2.append (theta_current[1])
      theta3.append (theta_current[2])

   
# Plot model and fitted data
My = []
for x in dx:
    My.append(model(x, theta_current))
#pylab.plot(dx, dy, "ro")
pylab.plot (dx, dy, "o", markerfacecolor='red', markeredgewidth=0.5, markeredgecolor='black')           
pylab.plot(dx, My, ".", markerfacecolor='blue', markeredgecolor='blue')
pylab.xlabel ('Time')
pylab.savefig('chain.pdf')
pylab.show()
print (theta_current)

fig, (ax1, ax2, ax3) = pylab.subplots(1, 3, figsize=(15,5))
ax1.hist(theta1, 30, color = 'lightblue', edgecolor = 'black',)
ax2.hist(theta2, 30, color = 'lightblue', edgecolor = 'black',)
ax3.hist(theta3, 30, color = 'lightblue', edgecolor = 'black',)
pylab.savefig ('chainDistrib.pdf')




