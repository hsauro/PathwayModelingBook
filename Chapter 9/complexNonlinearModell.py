import pylab as plt; import numpy as np
import lmfit; import tellurium as te 
import time; import copy; import random; import sys
import emcee
import time
import pickle
import pandas as pd  
        
nsims = 0

def saveSampleAsPickle (sample):
    with open ('samplePickle.pkl', 'wb') as f:
         pickle.dump (sample, f)
         
def loadSamplePickle ():
    with open('samplePickle.pkl', 'rb') as f:
         return pickle.load(f)
    
def loadIntoPandas (parameters, sample):
    df = pd.DataFrame (columns=parameters)
    for i in range (len (parameters)):
        df[parameters[i]] = sample[i]
    return df
    
def plotGrid (df):
    axes = pd.plotting.scatter_matrix(df, alpha=0.2, figsize=(10,10))
    for i in range(np.shape(axes)[0]):
        for j in range(np.shape(axes)[1]):
            if i < j:
               axes[i,j].set_visible(False)
    plt.savefig(r"c:\tmp\grid.pdf")
    
np.random.seed (int (time.time()))

np.random.seed (132)

r = te.loada("""      
# Reactions   
    reaction_1: $X0 -> S1; (Vm*X0)/((Km + X0) + (S1/KI));
    reaction_2: S1 -> S2;  k2*S1/(1 + S3/KI2);
    reaction_3: S2 -> S3;  k3*S2;
    reaction_4: S2 -> S4;  k4*S2;
    reaction_5: S4 -> $X1; k5*S4;
    reaction_6: S3 -> $X1; k6*S3; 

# Species initializations     
    $X0 = 10; S1 = 0
    S2 = 0
    S3 = 0
    S4 = 0
    $X1 = 10
# Parameters:    
    //Vm = 0;  Km = 0; KI = 0; k2 = 0
    //k3 = 0;  k4 = 0; k5 = 0; k6 = 0; KI2 = 10.1
    
   Vm = 15; Km = 5; KI = 10; k2 = 5; k3 = 10
   k4 = 5; k5 = 15; k6 = 5; KI2 = 10.1
""")

ground_truth = np.loadtxt('ground_truth.txt')
noisy_training_set = np.loadtxt('experimental_data.txt')

toFit = ['Vm', 'Km', 'KI', 'KI2', 'k2', 'k3', 'k4', 'k5','k6']; nParameters = len (toFit)

nDataPoints = 100
timeToSimulate = 2
# Create the experimental data
# First column is time, other columns are species
m = r.simulate (0, timeToSimulate, nDataPoints)

# Change this index to use a different variables
# These are the variables that will be used to fit the model
SIndexList = [1,2,3,4] # 1 = S1, 2 = S2, 3 = S3, 4 = S4
x_data = timeDim = ground_truth[:, 0] # Extract the time column

# Extract the SIndexList columns into y_data
y_data = []
for i in range (len(SIndexList)):
    y_data.append (ground_truth[:,SIndexList[i]])
    
# Create the 'experimental' data by adding noise
y_noise = np.empty([nDataPoints])
for k in range (len (SIndexList)):
   for i in range (0, len (y_data[k])):
       y_noise[i] = 0.1 # standard deviation of noise
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
#def weightedResiduals(p):
#    return (y_data - my_ls_func (p))/y_weight

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
for i in range (nParameters):
    params.add(toFit[i], value= 1.0, min=0, max=30)


# Compute the fitted parameters
minimizer = lmfit.Minimizer(residuals, params)
result = minimizer.minimize(method='differential_evolution')#'leastsqr')
lmfit.report_fit(result.params, min_correl=0.5)
result = minimizer.minimize(method='leastsqr')
lmfit.report_fit(result.params, min_correl=0.5)

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
ldata, = plt.plot (x_data, y_data[0], 'dm', markersize=8)
for k in range (1, len (SIndexList)):
    ldata2, = plt.plot (x_data, y_data[k], 'dm', markersize=8)

# Plot the fitted lines for S1, S2 and S3
# Retrieve lfit to use in the legend
lfit, = plt.plot (m[:,0], m[:,1], '-g', linewidth=2)
plt.plot (m[:,0], m[:,2], '-g', linewidth=2)
plt.plot (m[:,0], m[:,3], '-g', linewidth=2)
plt.plot (m[:,0], m[:,4], '-g', linewidth=2)

# Plot the residuals
resids = unWeightedResiduals(result.params)
lresids, = plt.plot (x_data, resids, 'bo', markersize=6)
plt.vlines(x_data, [0], resids, color='r', linewidth=2)

theResiduals = copy.deepcopy (resids)
#finalFittedData = copy.deepcopy (y_data)
originalYData = copy.deepcopy (y_data)

plt.tick_params(axis='both', which='major', labelsize=16)
plt.xlabel('Time')
plt.ylabel("Concentration", fontsize=16)
plt.legend([ldata, lfit, lresids],['Data', 'Best fit', 'Residuals'], loc=0, fontsize=10)
plt.axhline (y=0, color='k')
plt.savefig('fittedCurves.pdf')
plt.show()
 
to = time.time()
if True:
    pSamples = [] # Vm, Km, KI, KI2, k2, k3, k4, k5, k6
    for i in range (nParameters):
        pSamples.append ([])
    
    NSamples = 500
    
    print ("\nStart Monte Carlo Estimation")
    
    chis = []
    # Start the Monte Carlo parameter confidence estimation
    for n in range (NSamples): 
        if n % 100 == 0:
           print (n)
           
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

if False:
    to = time.time()
    ci = lmfit.conf_interval(minimizer, result)
    print ('Time for conf Interval = ', time.time() - to)
    lmfit.printfuncs.report_ci(ci)
    #
    cx, cy, grid = lmfit.conf_interval2d(minimizer, result, toFit[0], toFit[1], 100, 100)
    plt.contourf(cx, cy, grid, np.linspace(0, 1, 11))
    plt.xlabel(toFit[0])
    plt.colorbar()
    plt.ylabel(toFit[1])

if False:
    np.set_printoptions(precision=4, linewidth=150)
    
    print (result.covar)
    
    
    to = time.time()
    res = lmfit.minimize(residuals, method='emcee', nan_policy='omit', burn=500, steps=10000, thin=20,
                             params=params, is_weighted=False)
    import corner
    corner.corner(res.flatchain, labels=res.var_names, truths=list(res.params.valuesdict().values()), range=[(0,0.3),(0,1.2), 1])
    print ('Time for emcee = ', time.time() - to)

