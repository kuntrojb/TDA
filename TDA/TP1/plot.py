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
t_n_squared_fit = n_squared(n, *n_squared_fit)

plt.loglog(n, t, 'x', label='Gale Shapley',
           basex=2, basey=2)

# fitting
plt.loglog(n, t_n_squared_fit,
           basex=2, basey=2)

plt.xlabel('tamaño del vector')
plt.ylabel('tiempo de ejecución (segundos)')
plt.legend()
plt.savefig('tiempos.png')
plt.show()
