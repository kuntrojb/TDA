#!/usr/bin/env python

import numpy as np
import scipy
from matplotlib import pyplot as plt
from scipy import optimize

n_fft, t_fft = np.loadtxt('datosFFT.txt', unpack=True)

def n_squared(x, c, d, f):
    return c * (x*x)

def nlogn(x, c):
    return c*x*np.log2(x)

n_squared_fit, cov = optimize.curve_fit(n_squared, n_dft, t_dft)
t_n_squared_fit = n_squared(n_fft, *dft_fit)

plt.loglog(n_dft, t_dft, 'x', label='DFT',
           basex=2, basey=2)
# fitting
plt.loglog(n_fft, t_dft_fit,
           basex=2, basey=2)
plt.xlabel('tamaño del vector')
plt.ylabel('tiempo de ejecución (segundos)')
plt.legend()
plt.savefig('tiempos.png')
plt.show()
