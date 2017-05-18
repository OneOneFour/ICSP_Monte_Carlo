import time

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as scint

startTime = time.time()


def lotkarra(s, t, alp, bet, gam, delt):
    x, y = s
    dsdt = [alp * x - bet * x * y, delt * x * y - gam * y]
    return dsdt


alp, bet, gam, delt = 1, 0.2, 0.6, 1
t = np.linspace(0, 10, 1000)
plt.gca().set_xlabel("Time")
plt.gca().set_ylabel("Predator count")
s0 = [1, 1]
ans = scint.odeint(lotkarra, s0, t, args=(alp, bet, gam, delt))
plt.plot(t, ans[:, 0], linewidth=1, label="prey")
plt.plot(t, ans[:, 1], linewidth=1, label="pred")
plt.legend()
print(time.time() - startTime)
plt.show()
