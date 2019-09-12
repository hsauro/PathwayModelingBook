import numpy as np
import pylab
import statsmodels.api as sm

# Residual data for S1 and S2
S1 = np.array([1.25646491, 0.947882566, 0.397358056,0.335372002,  0.245941357, 0.155918422,
       -0.556750428, -0.591033227, -0.659627676, -1.41856797, -1.97506809])

S2 = np.array([-0.648710057, 1.01931184, -0.521154398,  -0.159291555, 0.641344813,
            -0.067860512, -0.663673399,  1.10483282, 0.796177025, -1.78660179,
            1.36881988])

pylab.figure(figsize=(9, 4))
pylab.subplot(1, 2, 1)
probplot1 = sm.ProbPlot(S1) # Compute the probability plot data
probplot2 = sm.ProbPlot(S2)

pylab.title('Q-Q Plot')
pylab.ylim(-2,2); pylab.xlim(-2,2)
pylab.plot (probplot1.theoretical_quantiles, probplot1.sample_quantiles, 's', color='blue', label='S1')
pylab.plot ([-2,2], [-2,2], 'red')
pylab.xlabel('z-score')
pylab.legend(); pylab.grid(True)

pylab.subplot(1, 2, 2)
pylab.title('Q-Q Plot')
pylab.ylim(-2,2); pylab.xlim(-2,2)
pylab.plot (probplot2.theoretical_quantiles, probplot2.sample_quantiles, 'o', color='green', label='S2')
pylab.plot ([-2,2], [-2,2], 'red')
pylab.legend(); pylab.grid(True)
pylab.xlabel('z-score')
pylab.ylabel('Sample Quantiles')
pylab.tight_layout()
pylab.savefig ('probplot.pdf')
pylab.show()
