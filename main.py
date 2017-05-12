import scipy.integrate as scint
import numpy as np
import time
import matplotlib.pyplot as plt
startTime = time.time()
def lotkarra(s,t,alp,bet,gam,delt):
    x,y = s
    dsdt = [alp*x - bet * x*y,delt * x * y - gam * y]
    return dsdt

alp,bet,gam,delt = 0.66,1.33,1,1
t = np.linspace(0,10,1000)
plt.gca().set_xlabel("Time")
plt.gca().set_ylabel("Predator count")
for i in np.arange(0.5,1.5,0.2):
    s0 = [i,i]
    ans = scint.odeint(lotkarra, s0, t, args=(alp, bet, gam, delt))
    plt.plot(t,ans[:,1],linewidth=1,label=i)
plt.legend(bbox_to_anchor=(1, 1), loc=2)
print(time.time() - startTime)
plt.show()
