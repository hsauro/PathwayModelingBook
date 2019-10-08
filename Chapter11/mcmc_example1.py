# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 19:31:48 2019

@author: hsauro
"""

import math, numpy as np, time
import pylab, scipy.stats

np.random.seed (1232)
# Generate some synthetic data
dx=[]
dy=[]

theta = [20, 6, 0.4]
for x in np.arange (0, 40, 0.5):
    dx.append (x)
    dy.append (np.random.normal(theta[0]+theta[1]*math.sin(2.*math.pi/24.*x+theta[2]), 2))

pylab.plot (dx, dy)
pylab.show()
   
np.random.seed(int (time.time()))
 
# Fit this Model to the data
def model (x,theta):
   return theta[0] + theta[1]*math.sin((2.0*math.pi/24.0)*x + theta[2])

# Chi Squared
def chi2(dx, dy, theta):
   s = 0.0
   for i in range(len(dx)):
      s += (model(dx[i], theta) - dy[i])**2
   t = s/len (dx)
   return t

# Likelihood function
def P(dx, dy, theta):
   #return -chi2(dx, dy, theta)
   return math.exp (-chi2(dx, dy, theta))

# Initial guess for model parameters
theta1 = []; theta2 = []; theta3 = []
theta_current = [0.,0.,0.]
theta_proposed = [0.,0.,0.]
P_current = P(dx, dy, theta_current)
chain = []
for i in range(40000):
   theta_proposed = [theta_current[0]+0.1*np.random.randn(),
                     theta_current[1]+0.1*np.random.randn(),
                     theta_current[2]+0.1*np.random.randn()]

   P_proposed = P (dx, dy, theta_proposed)
   ratio = min (1, P_proposed/P_current)
   
   r = np.random.rand()
   if ratio > r:
      theta_current = theta_proposed
      P_current = P_proposed
   if i >= 10000: # save chain only after burnin
      chain.append(theta_current)
      theta1.append (theta_current[0])
      theta2.append (theta_current[1])
      theta3.append (theta_current[2])

   
# Plot model and fitted data
My = []
for x in dx:
    My.append(model(x, theta_current))

pylab.plot (dx, dy, "o", markerfacecolor='red', markeredgewidth=0.5, markeredgecolor='black')           
pylab.plot(dx, My, ".", markerfacecolor='blue', markeredgecolor='blue')
pylab.xlabel ('Time')
#pylab.savefig('fitted.pdf')
pylab.show()

fig, (ax1, ax2, ax3) = pylab.subplots(1, 3, figsize=(15,5))
ax1.hist(theta1, 30, color = 'lightblue', edgecolor = 'black',)
ax2.hist(theta2, 30, color = 'lightblue', edgecolor = 'black',)
ax3.hist(theta3, 30, color = 'lightblue', edgecolor = 'black',)
pylab.savefig ('chainDistrib.pdf')
pylab.show()

print (np.mean (theta1), np.mean (theta2), np.mean (theta3))
print ("Theta 1 = ", np.percentile (theta1, 2.5), " 95% Percentaile = ", np.percentile (theta1, 97.5))
print ("Theta 2 = ", np.percentile (theta2, 2.5), " 95% Percentaile = ", np.percentile (theta2, 97.5))
print ("Theta 3 = ", np.percentile (theta3, 2.5), " 95% Percentaile = ", np.percentile (theta3, 97.5))

# Create a histogram for each parameter
hist1 = np.histogram(theta1, bins=100)
hist2 = np.histogram(theta2, bins=100)
hist3 = np.histogram(theta3, bins=100)

# Convert the histogram into a distribution function
theta1_dist = scipy.stats.rv_histogram (hist1)
theta2_dist = scipy.stats.rv_histogram (hist2)
theta3_dist = scipy.stats.rv_histogram (hist3)

# Draw a samples for each parameter
thetaList = []
# Create 20 0sets of thetas
for i in range (200):
    t1 = theta1_dist.rvs()
    t2 = theta2_dist.rvs()
    t3 = theta3_dist.rvs()
    thetaList.append ([t1, t2, t3])    
    
xd = []
ydmean = []; ydpercentile_plus = []; ydpercentile_minus = []
for x in np.arange (0, 40, 1):
    yd = []
    xd.append (x); 
    for i in range (100):
        yd.append (model (x,thetaList[i]))
    ydmean.append (np.mean (yd))
    ydpercentile_plus.append (np.percentile (yd, 97.5))
    ydpercentile_minus.append (np.percentile (yd, 2.5))
   
# PLot envelope graph
pylab.plot (xd, ydmean, 'k-')
pylab.fill_between(xd, ydpercentile_minus, ydpercentile_plus, color='orange', alpha=0.4)
pylab.savefig ('ShadedEnvelope.pdf')
pylab.show()

# PLot solution multiple lines
for i in range (100):
   xd = []; yd = []
   for x in np.arange (0, 40, 1):
       xd.append (x); 
       yd.append (model (x,thetaList[i]))
   pylab.plot (xd, yd, alpha=0.2, color='royalblue')
pylab.show()
  
# PLot scatter of solutions at each data point 
for i in range (50):
   xd = []; yd = []
   for x in np.arange (0, 40, 1.5):
       xd.append (x); 
       yd.append (model (x,thetaList[i]))
   pylab.scatter (xd, yd, alpha=0.2, color='firebrick')
pylab.show()   
        




