#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize

# n, t = np.loadtxt('datos.txt', unpack=True)

# (1,     733,    543,    0.6487290859222412, 0.5316669940948486)
# (10,    4987,   3788,   0.7539224624633789, 1.3273241519927979)
# (100,   45423,  36359,  2.403543472290039,  5.396233797073364)
# (500,   293931, 219462, 42.17999482154846,  41.373615980148315)
# (800,   560904, 413287, 147.21415662765503, 121.499107837677)

n = [733, 4987, 45423, 293931, 560904]
t = [0.6487290859222412, 0.7539224624633789, 2.403543472290039, 42.17999482154846, 147.21415662765503]

n = [543, 3788, 36359, 219462, 413287]
t = [0.5316669940948486, 1.3273241519927979, 5.396233797073364, 41.373615980148315, 121.499107837677]

def n_squared(x, c, d):
    return c * (x * x) + d

def nlogn(x, c):
    return c * x * np.log2(x)


n_squared_fit, cov = optimize.curve_fit(n_squared, n, t)
n2 = np.linspace(min(n), max(n), 50)
t_n_squared_fit = n_squared(n2, *n_squared_fit)

n_squared_fit, cov = optimize.curve_fit(nlogn, n, t)
n2 = np.linspace(min(n), max(n), 50)
t_n_squared_fit = nlogn(n2, *n_squared_fit)


plt.loglog(n, t, 'x', label='Resultado de la ejecucción',
           basex=2, basey=2)

# fitting
plt.loglog(n2, t_n_squared_fit, label='$O(n\\log n)$',
           basex=2, basey=2)

#plt.plot(n, t, 'x', label='Gale Shapley')

# fitting
#plt.plot(n, t_n_squared_fit)

plt.xlabel('Bytes del mensaje')
plt.ylabel('tiempo de ejecución (segundos)')
plt.legend()
plt.savefig('tiempo_descompresion.png')
plt.show()
