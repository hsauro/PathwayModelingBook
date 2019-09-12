import numpy as np
import matplotlib.pyplot as plt
import tellurium as te

Y, X = np.mgrid[-4:4:100j, -4:4:100j]

r = te.loada('''
    x' = 0*x + 1*y;
    y' = -1.2*x + 0.2*y;
    
    x = -0.3; y = -0.1;
''')

m = r.simulate (0, 25, 100)

U =  0*X + 1*Y
V = -1.2*X + 0.2*Y

plt.subplots(1,2, figsize=(10,4))
plt.subplot(121)
plt.xlabel('x', fontsize='16')
plt.ylabel('y', fontsize='16')
plt.streamplot(X, Y, U, V, density=[1, 1])

plt.ylim((-4,4))
plt.xlim((-4,4))

plt.axhline(0, color='black')
plt.axvline(0, color='black')

plt.subplot(122)

plt.ylim((-6,6))
plt.xlim((0,25))
plt.xlabel('Time', fontsize='13')


plt.plot (m[:,0], m[:,1], color='r', linewidth=2, label='x')
plt.plot (m[:,0], m[:,2], color='b', linewidth=2, label='y')
plt.legend()

plt.savefig ('c:\\tmp\\phase.pdf')

plt.show()
