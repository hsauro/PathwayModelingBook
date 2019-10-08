#
# Plot for generating Figures 10.8, 10.9 and 10.10 of the Pathway Modeling book
#
import pylab as plt; import numpy as np
import lmfit; import tellurium as te 
import time; import copy; import random; import sys
import emcee
import time

# Fix the data, not change in the errors in the data between runs
np.random.seed (126)
#np.random.seed (2)

nsims = 0

r = te.loada("""
   S1 -> S2; k1*S1;
   S2 -> S3; k2*S2;
   
   S1 = 1; S2 = 0; S3 = 0; 
   k1 = 0.45; k2 = 0.15; 
""")

toFit = ['k1', 'k2']; nParameters = len (toFit)

nDataPoints = 32
timeToSimulate = 20
# Create the experimental data
# First column is time, other columns are species
m = r.simulate (0, timeToSimulate, nDataPoints)

# Plot ground truth
plt.figure(figsize=(7,5))
plt.plot (m['time'], m['[S1]'], linewidth=3, label='S1')
plt.plot (m['time'], m['[S2]'], linewidth=3, label='S2')
plt.plot (m['time'], m['[S3]'], linewidth=3, label='S3')
plt.xlabel('Time', fontsize=18)
plt.ylabel('Concentation', fontsize=18)
plt.legend (fontsize=18)
plt.savefig  ('c:\\tmp\\groundtruth_simpleModel.pdf')
plt.show()

# Change this index to use a different variables
# These are the variables that will be used to fit the model
SIndexList = [3] # 1 = S1, 2 = S2, 3 = S3
x_data = m['time']; # Extract the time column

# Extract the SIndexList columns into y_data
y_data = []
for i in range (len(SIndexList)):
    y_data.append (m[:,SIndexList[i]])
    
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

# Plot ground truth
#plt.figure(figsize=(7,5))
index = 0
for i in SIndexList:
    plt.plot (m['time'], y_data[index], 'or', linewidth=3, label='S' + str (SIndexList));
    plt.xlabel('Time', fontsize=18)
    plt.ylabel('Concentation', fontsize=18)
    plt.legend (fontsize=18)
    plt.savefig  ('c:\\tmp\\groundtruthS' + str (i) + '.pdf')
    plt.show()
    index = index + 1


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
   
# Randomize the work of the optimizer
rd = int (time.time())
print ('Random number = ', rd)
np.random.seed (rd)

# Set up the parameters that we will fit
params = lmfit.Parameters()
params.add('k1', value=1, min=0, max=10)
params.add('k2', value=1, min=0, max=10)

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
# Boostrapping analysis
if True:
    k1Sample = []; k2Sample = []; NSamples = 6000
    
    print ("\nStart Monte Carlo Estimation")
    
    chis = []
    to = time.time()
    nsims = 0
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
           k1Sample.append (pp['k1'])
           k2Sample.append (pp['k2'])
        else:
           print (result.redchi)
 
    
    print ("Finished Monte Carlo Estimation.....")
    if len (k1Sample) == 0:
        print ("Failed to compute Monto Carlo estimate, unable to generate fits, bad model or insufficient data")
        sys.exit("Unable to continue")
 
    print ('Time for Bootstrap = ', time.time() - to)
    print ('Number of simulations = ', nsims)

    # Compute the mean values of the k1 and k2 samples
    meank1 = np.mean (k1Sample); meank2 = np.mean (k2Sample)
    
    # Compute 95% percentiles
    plusk1 = np.percentile (k1Sample, 97.5) - meank1
    minusk1 = meank1 - np.percentile (k1Sample, 2.5)
    
    plusk2 = np.percentile (k2Sample, 97.5) - meank2
    minusk2 = meank2 - np.percentile (k2Sample, 2.5)

    # Note that the limits are not symmetric
    print ('Computed 95 percent percentiles from the Monte Carlo run:')
    print ('k1: ', meank1, "+/- ", plusk1, minusk1)
    print ('k2: ', meank2, "+/- ", plusk2, minusk2)
    
    plt.hist (k1Sample, 10, range=[0,1], color='peachpuff')
    plt.ylabel('Frequency'); 
    plt.xlabel ('k1'); plt.title ('k1 variation')
    plt.savefig('k1Distribution.pdf')
    plt.show()
    plt.hist (k2Sample, 10, range=[0,1], color='peachpuff')
    plt.ylabel('Frequency'); 
    plt.xlabel ('k2'); plt.title ('k2 variation');
    plt.savefig('k2Distribution.pdf')
    plt.show()
    
    # Scatter plot of k1 versus k2
    plt.xlim((0.2, 0.65)); plt.ylim ((0.0, 0.3))
    plt.plot (k1Sample, k2Sample, '.', color='cornflowerblue')
    plt.xlabel ('k1'); plt.ylabel ('k2')
    plt.title ('Scatter plot of k1 against k2')
    plt.savefig('k1_k2_scatter.pdf')
    plt.show()
print ('Time for monte carlo = ', time.time() - to)


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

to = time.time()
# MCMC Analysis
if False:
    nsims = 0
    np.set_printoptions(precision=4, linewidth=150)
    
    print (result.covar)  
    
    from tqdm import tqdm
    to = time.time()
    res = minimizer.emcee(params=params,burn=5000, steps=15000, thin=20,is_weighted=False,progress=True)
    #res = lmfit.minimize(residuals, method='emcee', nan_policy='omit', burn=500, steps=5000, thin=20, progress=True,
    #                         params=params, is_weighted=False)
    import corner
    print('Plot results of emcee...')
    corner.corner(res.flatchain, labels=res.var_names, truths=list(res.params.valuesdict().values()), range=[(0,0.3),(0,1.2), 1])
    plt.savefig ('c:\\tmp\emcee.pdf')
    print ('Time for emcee = ', time.time() - to)
    print ('Number of simulations = ', nsims)
