import time

import numpy as np
import scipy.integrate as scint

startTime = time.time()


def lotkarra(s, t, alp, bet, gam, delt):
    x, y = s
    dsdt = [alp * x - bet * x * y, delt * x * y - gam * y]
    return dsdt


def lotkavolterragraph(alpha, beta, gamma, delta, s0, stop=10, steps=10):
    t = np.linspace(0, stop, steps * stop)
    ans = scint.odeint(lotkarra, s0, t, args=(alpha, beta, gamma, delta))
    return (ans, t)
