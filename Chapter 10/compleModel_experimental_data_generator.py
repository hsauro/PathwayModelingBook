# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 22:29:14 2018

@author: Veronica Porubsky, modified by Herbert Sauro (August 2019)

Title: Experimental Data Generator
"""
import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import roadrunner as rd
import random
import os
#%% Create new director 'parameter_fitting_tutorial' for program output
current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'parameter_fitting_tutorial')
if not os.path.exists(final_directory):
   os.makedirs(final_directory)   
   
r = te.loada("""       
# Reactions   
    J1: $X0 -> S1; (Vm*X0)/((Km + X0) + (S1/KI));
    J2: S1 -> S2; k2*S1/(1 + S3/KI2);
    J3: S2 -> S3; k3*S2;
    J4: S2 -> S4; k4*S2;
    J5: S4 -> $X1; k5*S4;
    J6: S3 -> $X1; k6*S3;
  
# Species initializations
    $X0 = 10; S1 = 0; S2 = 0;  S3 = 0;  S4 = 0
    $X1 = 10

# Parameters:  
    Vm = 15; Km = 5; KI = 10; k2 = 5; 
    KI2 = 10.1; k3 = 10; k4 = 5;  k5 = 15; k6 = 5;  
    
""")
#------------------------------------------------------------
# Simulate model to obtain the ground truth
r.reset() 
result = r.simulate(0, 2, 100)   
r.plot()
#------------------------------------------------------------
#  Export ground truth simulation data
mat = np.matrix(result)
with open(os.path.join(final_directory,'ground_truth.txt'),'wb') as f:
    for line in mat:
        np.savetxt(f, line, fmt='%.7f')
#%% Generate noisy data from the ground truth simulation with user-specified percentage of noise
#--------------------------------------------------------------------------------------------
#   The user will specify what percent noise they wish to add and this percentage will be multiplied 
#   by the ground truth data at each time for a given species to produce a standard deviation.
#   The noise at each time point will be determined by drawing a random number from a normal distribution 
#   with a mean of zero and the standard deviation defined by the specified percentage.        
time2 = result[:, 0]
training_set = result[:, 1:5]
user_input = False
while user_input == False:
    try:
        percent_noise = input('Please specify the percent noise desired to produce the noisy training data. Enter a percentage between 0 and 100: ')
        if 0 <= percent_noise <= 100:
            user_input = True
        elif 100 <= percent_noise or percent_noise <= 0:
            print('You must enter a percentage between 0 and 100.')
    except:
        print('You must enter a percentage between 0 and 100.')
percent_noise = percent_noise/100.0
# random.normalvariate(mu, sigma)) with mean zero and standard deviation of 5% of the value.
noisy_training_set = np.zeros((25,5))
for k in range(1, 5):
    for i in range(25):
        noisy_training_set[i, k] = training_set[i*4, k-1] + random.normalvariate(0, percent_noise*training_set[i*4, k-1])
        noisy_training_set[i, 0] = time2[i*4]
plt.figure(1)
plt.title('25 Datapoints from Each Model Species Timecourse with Noise Added') 
plt.ylabel('Species Concentrations (nM)', fontsize='12') 
plt.xlabel('Time (s)', fontsize='12')
plt.gca().set_color_cycle(['c', 'm', 'b', 'r'])
plt.plot(noisy_training_set[:, 0], noisy_training_set[:, 1:5], '.')  
plt.savefig ('rawdata.pdf')     
#--------------------------------------------------------------------------------------------
#   Export noisy simulation data as the "experimental data" for parameter fitting tutorial
mat = np.matrix(noisy_training_set)
with open(os.path.join(final_directory, 'experimental_data.txt'),'wb') as f:
    for line in mat:
        np.savetxt(f, line, fmt='%.7f')
