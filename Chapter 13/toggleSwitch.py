# Toggle switch, nullcline and phase portrait
import numpy as np, matplotlib.pyplot as plt
import tellurium as te

Y, X = np.mgrid[0:8:200j, 0:8:200j]
U, V = np.mgrid[0:8:200j, 0:8:200j]

r = te.loada('''
    J1: -> x; k1/(1+y^n1) - k2*x;
    J2: -> y; k3/(1+x^n2) - k4*y;

    x = 4; y = -4;
    k1 = 12; k3 = 12; k2 = 2; k4 = 2
    n1 = 4; n2 = 4
''')

for idx in range (200):
    for idy in range (200):
        r.x = X[idx,idy];  r.y = Y[idx,idy]
        U[idx,idy] = r["x'"]
        V[idx,idy] = r["y'"]

plt.subplots(1,2, figsize=(8,6))
plt.subplot(111)
plt.xlabel('x', fontsize='16')
plt.ylabel('y', fontsize='16')
plt.streamplot(X, Y, U, V, density=[2, 2])

# Plot the nullclines
nullcline_x = np.linspace(0, 8, 200)
nullcline_y = (12 / (1 + nullcline_x**4))/2
plt.plot(nullcline_x, nullcline_y, lw=4, color='red')

nullcline_y = (12 / (1 + nullcline_x**4))/2
plt.plot(nullcline_y, nullcline_x, lw=4, color='red')

plt.plot(0, 6, '.', color='green', markersize=20)
plt.plot(6, 0, '.', color='green', markersize=20)
plt.plot(1.36, 1.36, '.', color='green', markersize=20)

plt.ylim((0,7))
plt.xlim((0,7))

plt.savefig ('phase.pdf')
plt.show()
