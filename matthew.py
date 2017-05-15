import scipy.misc as scm
import numpy.random as npr
import numpy as np
import matplotlib.pyplot as plt

def culmBinom(p, n, rand):
    s = 0
    prob = 1
    while (1):
        prob -= (p**(n-s))*((1-p)**s)*(scm.comb(n, s))
        if rand > prob:
            return(s)
        else:
            s += 1

g = 100
p = 0.5

values = np.zeros(g+1)
for x in range(100000):
    values[culmBinom(p, g, npr.uniform())] += 1

plt.plot(range(g+1), values)

plt.show()
