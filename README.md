# ICSP Monte Carlo
A simulation of how animal populations change over time using the Monte-Carlo method and the Lotkarra-Voltara equations. First Year IC summer project by Robert King and Matthew Cotton

**File Guide:**

  *monte.py*  -  contains the code that creates the objects of world, predators and prey, with their respective processes (e.g. movement, birth, death etc.
  *graphics.py*  -  contains the code that manages the running of the simulation, contains the main algorithm. Generates the GUI.
  *projectfunctions.py*  -  contains functions tailored to the project 
  
  **Comments:**
  
  DNF - did not finish. Refers to an extension that was started but that is currentlly not completely finished.



**Lotka-Volterra Equations**

  The starting point for this project was the Lotka-Volterra equations which are used to simulate how the populations of a predator and a prey species evolve over time. The Lotka-Volterra equations assume an enviroment where all predators and prey can interact with one another and where there is a *suitably* large inital population of both species such that the populations can be treated as continous variables (whereas in reality they are actually discrete). 
 
  One of the first things we undertook in this project was to create a set of plots to test the Lotka-Volterra model. These were created in python 3.0 using matplotlib and scipy, both free and open source libraries.
  
  
  ```python
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
    return (t, ans)
  ```
