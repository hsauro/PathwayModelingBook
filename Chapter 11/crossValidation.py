import numpy as np, pylab as plt

np.random.seed (127)

def gendata():
    y = []
    x = np.arange (-1, 2.5, 0.1)
    for value in x:
        y.append (1.1*value*value*value - 2.3*value*value + 1.1*value + 2 + np.random.normal (0, 2))
    return [x, y]   

[x, y] = gendata()
xn = copy.copy (x); yn = copy.copy (y)

av = []
polylist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
fig, ax = plt.subplots(nrows=4, ncols=4, figsize=(11,9))

count = 1
# Try the differen models
for p in polylist:
    
    fu = []
    for i in range (len (x)):
        xfit = copy.copy (xn); yfit = copy.copy (yn)
        # Remove a data point
        xfit = np.delete (xfit, i)
        yfit = np.delete (yfit, i)
        f1 = np.polyfit (xfit, yfit, p)
        polyfunc = np.poly1d (f1)
        # Keep a record of the fitted model
        fu.append (polyfunc)
        rmse = (polyfunc (xn[i]) - yn[i])**2
      
    # Compute average rmse
    av.append (rmse/len (x))
    
    plt.subplot (4,4, count)
    plt.plot (xn, yn, 'o', markersize=4)
    for f in fu:
        plt.plot (x, f(x))
    count = count + 1
plt.savefig ('cross.pdf')

plt.plot (x, y, 'o'); plt.show()      
plt.plot (polylist[0:8], av[0:8])
plt.savefig('avcross.pdf')
