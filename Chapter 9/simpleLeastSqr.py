from scipy import *
from scipy import optimize
# Declare the experimental data
x = array([0, 10, 20, 50, 100, 200, 400])
y = array([0, 9, 10, 17, 18, 20, 19])

# Define the objective function
def residuals (p):
    [vmax,Km] = p
    return y - vmax*x/(Km+x)

# Fit the model to the data
output = optimize.leastsq (residuals, [10, 10])
