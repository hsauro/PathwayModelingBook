import numpy as np                           
import matplotlib.pyplot as plt   
from scipy.integrate import odeint
vo = 10                           
k1 = 0.5                          
k2 = 0.35 
                        
# Declare the model               
def myModel(y, t):                
   dy0 = vo - k1*y[0]                
   dy1 = k1*y[0] - k2*y[1]           
   return [dy0, dy1]   
                 
time = np.linspace(0.0, 20.0, 100)   
yinit = np.array([0.0, 0.0])         
y = odeint (myModel, yinit, time)  
plt.plot(time, y[:,0], time, y[:,1]) 
plt.xlabel('t')                                  
plt.ylabel('y')                                                       
plt.show()   
