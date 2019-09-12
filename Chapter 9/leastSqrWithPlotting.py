def peval(x, p):
    return p[0]*x/(p[1]+x)

Vmax,Km = 20,15
yTrue = Vmax*x/(Km+x)

import matplotlib.pyplot as plt
plt.plot(x, peval (x, output[0]), '--', x, y, 'o', x, yTrue,
    'r', x, residuals(output[0]), 'r^', markersize=10)
plt.title('Least-squares fit to noisy data')
# loc=10 means center the legend
plt.legend(['Fitted Curve', 'Noisy Data',
    'Underlying Function', 'Residuals'], loc=10)
plt.show()
