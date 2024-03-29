#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize

n, t = np.loadtxt('datos.txt', unpack=True)


def n_squared(x, c, d):
    return c * (x * x) + d


def nlogn(x, c):
    return c * x * np.log2(x)


n_squared_fit, cov = optimize.curve_fit(n_squared, n, t)
n2 = np.linspace(min(n), max(n), 50)
t_n_squared_fit = n_squared(n2, *n_squared_fit)


plt.loglog(n, t, 'x', label='Resultado de la ejecucción',
           basex=2, basey=2)

# fitting
plt.loglog(n2, t_n_squared_fit, label='$O(n^2)$',
           basex=2, basey=2)

#plt.plot(n, t, 'x', label='Gale Shapley')

# fitting
#plt.plot(n, t_n_squared_fit)

plt.xlabel('Cantidad de solicitantes')
plt.ylabel('tiempo de ejecución (segundos)')
plt.legend()
plt.savefig('tiempos.png')
plt.show()
