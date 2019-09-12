import numpy as np
import matplotlib.pyplot as plt
import tellurium as te

Y, X = np.mgrid[-4:4:100j, -4:4:100j]

r = te.loada('''
    x' = -2*x - 0*y;
    y' =  -0.15*x - 2*y;
    
    x = 4; y = -4;
''')


m = r.simulate (0, 8, 100)

U =  -2*X - 0*Y
V =  -0.15*X - 2*Y

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

plt.ylim((-5,5))
plt.xlim((0,5))
plt.xlabel('Time', fontsize='13')


plt.plot (m[:,0], m[:,1], color='r', linewidth=2, label='x')
plt.plot (m[:,0], m[:,2], color='b', linewidth=2, label='y')
plt.legend()

plt.savefig ('c:\\tmp\\phase.pdf')

plt.show()
