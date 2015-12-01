#!/usr/bin/env python
import sys
from numpy.random import normal, sample, choice
from scipy.stats import norm
from numpy import var
from math import sqrt, log
from matplotlib import pyplot as plt

if len(sys.argv) < 6 or len(sys.argv) % 2 == 1:
    print("Usage: ./gaussian_mix_em.py samples_per_dist mean_1 var_1 mean_2 var_2 [...mean_n var_n]")
    sys.exit(0)

samples = int(sys.argv[1])
means = [float(m) for i,m in enumerate(sys.argv) if i % 2 == 0 and i >= 2]
variances = [float(m) for i,m in enumerate(sys.argv) if i % 2 == 1 and i >= 2]
dists = len(means)
iterations = 500

# assert(len(means) == len(variances))

data = []
for i, m in enumerate(means):
    [data.append(normal(m,sqrt(variances[i]))) for _ in range(samples)]

print("Generated "+str(len(data))+" data points.")
f1 = plt.figure()
plt.hist(data,bins=50)
f1.show()

def generate_initial(data):
    means = [choice(data) for _ in range(dists)]
    variances = [var(choice(data,2)) for _ in range(dists)]
    pi = [1.0/dists for _ in range(dists)]

    return means, variances, pi

em_means, em_vars, pi = generate_initial(data)
#sPi = sum(pi)
#pi = [i/sPi for i in pi]
print("Randomly estimated means: "+str(em_means))
print("Variances: "+str(em_vars))
print("Contribution: "+str(pi))
print("Data: "+str(data))

print("Starting EM iterations...\n")

def E_step(data,means,variances,pis):
    resps = [[] for _ in means]
    for i,m in enumerate(means):
        for elm in data:
            r_up = pis[i]*norm.pdf(elm,loc=m,scale=variances[i])
            r_down = sum([pis[j]*norm.pdf(elm,loc=means[j],scale=variances[j]) for j in range(len(means))])
            resps[i].append(r_up/r_down)
    return resps
    
def M_step(resps,data,nodists):
    res = {'means':[],'variances':[],'pis':[]}
    for j in range(nodists):
        m_up = sum([resps[j][i]*data[i] for i in range(len(data))])
        m_down = sum([resps[j][i] for i in range(len(data))])
        t_mean = m_up/m_down
        res['means'].append(t_mean)

        v_up = sum([resps[j][i]*pow(data[i] - t_mean,2) for i in range(len(data))])
        v_down = m_down
        t_var = v_up/v_down
        res['variances'].append(t_var)

        res['pis'].append(sum(resps[j])/len(data))

    return res

def log_likelihood(data,pis,means,variances):
    ll = sum([log(pis[j]*norm.pdf(elm,loc=means[j],scale=variances[j]) or 1) for elm in data for j in range(len(pis))
              if pis[j] != 0 if variances[j] != 0])
    return ll

def max_error_rate(old,new):
    er = max([abs(old[i]-new[i])/old[i] for i in range(len(old))])
    return er

olgl = None
i = 0
while i < iterations:
    lgl = log_likelihood(data,pi,means,variances)
    try:
        resps = E_step(data,means,variances,pi)
        nps = M_step(resps,data,dists)
    except:
        print("Found error...")
        means, variances, pi = generate_initial(data)
        i = 0
        continue
    means = nps['means']
    variances = nps['variances']
    i += 1
    print("Iteration "+str(i)+" LogL: "+str(lgl)+".\nMean: "+str(means)+"\nVars: "+str(variances)+"\nPis: "+str(pi))
    print("Membership weights: \n"+str(resps)+"\n")
    pi = nps['pis']
    if olgl is not None and abs((lgl-olgl)/olgl) < 0.00001: break
    olgl = lgl

print("Ran a total of "+str(i+1)+" iterations.")
print("Pi: "+str(pi))
print("Means: "+str(means))
print("Vars: "+str(variances))
