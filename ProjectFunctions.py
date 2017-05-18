import scipy.misc as scm
import numpy.random as npr
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

def saveValues(a, b, c, d, fdir, text=1):
    fd = open(fdir,'a')
    if text:
        print("Found the file....")
    fd.write("{}, {}, {}, {}\n".format(a, b, c, d))
    if text:
        print("Saving....")
    fd.close()
    if text:
        print("Saved!")
