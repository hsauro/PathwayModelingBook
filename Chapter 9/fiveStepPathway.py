import pylab as plt; import numpy as np
import lmfit; import tellurium as te 
import time; import copy; import random; import sys
import emcee
import time
import pandas as pd  

# Call loadIntoPandas (toFit, pSamples)
def loadIntoPandas (parameters, sample):
    df = pd.DataFrame (columns=parameters)
    for i in range (len (parameters)):
        df[parameters[i]] = sample[i]
    return df
    
def plotGrid (df):
    axes = pd.plotting.scatter_matrix(df, alpha=0.2, figsize=(10,10))
    for i in range(np.shape(axes)[0]):
        for j in range(np.shape(axes)[1]):
            if (i < j):
               axes[i,j].set_visible(False)
            else:
                if i != j:
                   axes[i,j].set_xlim(0.0,8.0)
                   axes[i,j].set_ylim(0.0,8.0)

    plt.savefig(r"c:\tmp\grid.pdf")
    plt.show()
    
np.random.seed (int (time.time()))
#
#for i in range(5):
#    for j in range(5):
#        axS[i,j].set_xlim(0.0,1.0)
#        if i != j:
#             axS[i,j].set_ylim(0.0,1.0)
             
             
#np.random.seed (126)

np.random.seed (5)
r = te.loada("""      
# Reactions   
    J1: S1 -> S2; k1*S1
    J2: S2 -> S3; k2*S2
    J3: S3 -> S4; k3*S3
    J4: S4 -> S5; k4*S4
    J5: S5 -> S6; k5*S5;

# Species initializations     
    S1 = 10;
# Parameters:      
   k1 = 1; k2 = 2; k3 = 3; k4 = 4; k5 = 5
""")

toFit = ['k1', 'k2', 'k3', 'k4', 'k5'];
nParameters = len (toFit)

nDataPoints = 30
timeToSimulate = 4
nsims = 0

# Create the experimental data
# First column is time, other columns are species
m = r.simulate (0, timeToSimulate, nDataPoints)

# Change this index to use a different variables
# These are the variables that will be used to fit the model
SIndexList = [1,2,3,4,5,6] # 1 = S1, 2 = S2, 3 = S3
x_data = m['time'] # Extract the time column

# Extract the SIndexList columns into y_data
y_data = []
for i in range (len(SIndexList)):
    y_data.append (m[:,SIndexList[i]])
    
# Create the 'experimental' data by adding noise
y_noise = np.empty([nDataPoints])
for k in range (len (SIndexList)):
   for i in range (0, len (y_data[k])):
       y_noise[i] = 0.0 # standard deviation of noise
       # Might be better to use lognormal here?
       ln = np.random.normal (0, y_noise[i]);
       while y_data[k][i] + ln < 0: 
             ln = np.random.normal (0, y_noise[i]);        
       y_data[k][i] = y_data[k][i] + ln # Add noise


# Compute the simulation at the current parameter values
# Return the time series variable indicated by SIndex
# This is very inefficient since it has to be called for
# each variable we use to fit the model. Eg if SIndexList = [1,2,3]
# then we'll have to call this three times, ideally we should call
# it once and collect all SIndex variables at once. 
def computeSimulationData(p, SIndex):
    global nsims
    r.reset()  
    pp = p.valuesdict()
    for i in range(0, nParameters):
       r.model[toFit[i]] = pp[toFit[i]]
    m = r.simulate (0, timeToSimulate, nDataPoints)
    nsims = nsims + 1
    return m[:,SIndex]

# Compute the residuals between objective and experimental data
def residuals(p):
    global y_data, SIndexList
    y1 = (y_data[0] - computeSimulationData (p, SIndexList[0]));    
    y1 = np.concatenate ((y1, ))
    for k in range (1, len (SIndexList)):
        y1 = np.concatenate ((y1, (y_data[k] - computeSimulationData (p, SIndexList[k]))))
    return y1

def unWeightedResiduals(p):
    y1 = (y_data[0] - computeSimulationData (p, SIndexList[0]))
    return y1   
   
# Set up the parameters that we will fit
params = lmfit.Parameters()
for k in toFit:
    params.add(k, value=1, min=0, max=10)

# Compute the fitted parameters
minimizer = lmfit.Minimizer(residuals, params)
result = minimizer.minimize(method='differential_evolution')#'leastsqr')
lmfit.report_fit(result.params, min_correl=0.5)
result = minimizer.minimize(method='leastsqr')
lmfit.report_fit(result.params, min_correl=0.1)

# Assign fitted parameters to the model
r.reset()
for i in range(0, nParameters):
   r.model[toFit[i]] = result.params[toFit[i]].value
m = r.simulate (0, timeToSimulate, 100)

# Set up some convenient font sizes
plt.rcParams.update({'axes.titlesize': 16})
plt.rcParams.update({'axes.labelsize': 14})
plt.rcParams.update({'xtick.labelsize': 13})
plt.rcParams.update({'ytick.labelsize': 13})

# Plot experimental data
plt.figure (figsize=(7,5))
ldata, = plt.plot (x_data, y_data[0], 'o', markersize=6)
for k in range (1, len (SIndexList)):
    ldata2, = plt.plot (x_data, y_data[k], 'o', markersize=6)
plt.savefig('fiveStepsRawData.pdf')
plt.show()

plt.figure (figsize=(7,5))
ldata, = plt.plot (x_data, y_data[0], 'o', markersize=6)
for k in range (1, len (SIndexList)):
    ldata2, = plt.plot (x_data, y_data[k], 'o', markersize=6)

# Plot the fitted lines for S1, S2 and S3
# Retrieve lfit to use in the legend
# Set True if you want the fit plotted as well
if True:
  for k in r.getFloatingSpeciesConcentrationIds():
      lfit, = plt.plot (m['time'], m[k], '-', linewidth=2)

  # Plot the residuals
  resids = unWeightedResiduals(result.params)
  lresids, = plt.plot (x_data, resids, 'rv', markersize=6)
  plt.vlines(x_data, [0], resids, color='r', linewidth=2)

theResiduals = copy.deepcopy (resids)
originalYData = copy.deepcopy (y_data)

plt.tick_params(axis='both', which='major', labelsize=16)
plt.xlabel('Time')
plt.ylabel("Concentration", fontsize=16)
plt.legend([ldata, lfit, lresids],['Data', 'Best fit', 'Residuals'], loc=0, fontsize=10)
plt.axhline (y=0, color='k')
plt.savefig('fiveStepsFittedData.pdf')
plt.show()
 
nsims = 0

to = time.time()
# Boostrapping analysis
if True:
    to = time.time()
    if True:
        pSamples = [] # Vm, Km, KI, KI2, k2, k3, k4, k5, k6
        for i in range (nParameters):
            pSamples.append ([])
        
        NSamples = 2000
        
        print ("\nStart Monte Carlo Estimation")
        
        chis = []
        # Start the Monte Carlo parameter confidence estimation
        for n in range (NSamples): 
            if n % 100 == 0:
               print (n)
               
            # Generate new synthetic data set by randomly adding
            # the residuals values to the fitted data
            for j in range (len (y_data[0])):
                for i in range (len (SIndexList)):
                    y_data[i][j] = originalYData[i][j] + random.choice (theResiduals)
                   
            #result = minimizer.minimize(method='differential_evolution')
            result = minimizer.minimize(method='leastsqr')
            result = minimizer.minimize(method='leastsqr')
            if result.success == False:
                print ('Failed')
            # Not all fits will work so we test against a threshold   
            if result.redchi < 500: 
               chis.append (result.redchi)
               pp = result.params.valuesdict()
               # Collect the fitted parameters
               for i in range (nParameters):
                   pSamples[i].append (pp[toFit[i]])
            else:
               print (result.redchi)
               
        
        print ("Finished Monte Carlo Estimation.....")
        if len (pSamples[0]) == 0:
            print ("Failed to compute Monto Carlo estimate, unable to generate fits, bad model or insufficient data")
            sys.exit("Unable to continue")
     
        # Compute the mean values of the k1 and k2 samples
        mean = []
        for i in range (nParameters):
            mean.append([])
            mean[i] = np.mean (pSamples[i])
        
        # Compute 95% percentiles
        plus = []; minus = []
        for i in range (nParameters):
            plus.append (np.percentile (pSamples[i], 97.5) - mean[i])
            minus.append (mean[i] - np.percentile (pSamples[i], 2.5))
    
        # Note that the limits are not symmetric
        print ('Computed 95 percent percentiles from the Monte Carlo run:')
        for i in range (nParameters):
            print (toFit[i] + ': ', mean[i], "+/- ", plus[i], minus[i])
           
    print ('Time for monte carlo = ', time.time() - to)
    print ('Number of simulations = ', nsims)

    
# Chi Square Analysis
if False:
    to = time.time()
    ci = lmfit.conf_interval(minimizer, result)
    print ('Time for conf Interval = ', time.time() - to)
    lmfit.printfuncs.report_ci(ci)
    #
    cx, cy, grid = lmfit.conf_interval2d(minimizer, result, 'k1', 'k2', 100, 100)
    plt.contourf(cx, cy, grid, np.linspace(0, 1, 11))
    plt.xlabel('k1')
    plt.colorbar()
    plt.ylabel('k2')


# MCMC Analysis
if False:
    np.set_printoptions(precision=4, linewidth=150)
    
    print (result.covar)  
    
    from tqdm import tqdm
    to = time.time()
    res = minimizer.emcee(params=params,burn=500, steps=5000, thin=20,is_weighted=False,progress=True)
    #res = lmfit.minimize(residuals, method='emcee', nan_policy='omit', burn=500, steps=5000, thin=20, progress=True,
    #                         params=params, is_weighted=False)
    import corner
    print('Plot results of emcee...')
    corner.corner(res.flatchain, labels=res.var_names, truths=list(res.params.valuesdict().values()), range=[(0,0.3),(0,1.2), 1])
    plt.savefig ('c:\\tmp\emcee.pdf')
    print ('Time for emcee = ', time.time() - to)


