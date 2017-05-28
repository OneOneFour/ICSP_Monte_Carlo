import scipy.misc as scm
import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
def culmBinom(p, n):
    s = 0
    prob = 1
    rand = npr.uniform() #generates a random number to compare the probability to
    while (1):
        prob -= (p**s)*((1-p)**(n-s))*(scm.comb(n, s)) #adjust the parameters of prob to allow for the new number of events
        if rand > prob: #see if the randomly generated number lies in the region corresponding to s events
            return(s)   #if the randomly generated number lies within the section for this area of prob, retun the number of successes
        else:
            s += 1

def saveValues(a, b, c, d, prey0, pred0, fdir, text=1):
    fd = open(fdir,'a')
    if text:
        print("Found the file....")
    fd.write("{}, {}, {}, {}, {}, {}\n".format(a, b, c, d, prey0, pred0))
    if text:
        print("Saving....")
    fd.close()
    if text:
        print("Saved!")

def culmBinomNew(p, n):
    s = 0
    for i in range(n):
        if npr.rand() >= p:
            s += 1
    return s

def Graph(trials, events, p):
    old = np.zeros(events)
    new = np.zeros(events)

    for i in range(trials):
        #old[culmBinom(n,p)] += 1
        new[culmBinomNew(p, events)] += 1

    plt.plot(range(events), old)
    plt.plot(range(events), new)

    plt.show()
