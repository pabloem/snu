#!/usr/bin/env python
import sys
from numpy.random import normal, sample, choice
from scipy.stats import norm
from numpy import var
from math import sqrt
from matplotlib import pyplot as plt

if len(sys.argv) < 6 or len(sys.argv) % 2 == 1:
    print("Usage: ./gaussian_mix_em.py samples_per_dist mean_1 var_1 mean_2 var_2 [...mean_n var_n]")
    sys.exit(0)

samples = int(sys.argv[1])
means = [float(m) for i,m in enumerate(sys.argv) if i % 2 == 0 and i >= 2]
variances = [float(m) for i,m in enumerate(sys.argv) if i % 2 == 1 and i >= 2]
dists = len(means)
iterations = 10

# assert(len(means) == len(variances))

data = []
for i, m in enumerate(means):
    [data.append(normal(m,sqrt(variances[i]))) for _ in range(samples)]

print("Generated "+str(len(data))+" data points.")
"""
f1 = plt.figure()
plt.hist(data,bins=50)
f1.show()
"""

em_means = [choice(data) for _ in range(dists)]
em_vars = [var(choice(data,len(data)//dists)) for _ in range(dists)]
pi = [1.0/dists for _ in range(dists)]
#sPi = sum(pi)
#pi = [i/sPi for i in pi]
print("Randomly estimated means: "+str(em_means))
print("Variances: "+str(em_vars))
print("Contribution: "+str(pi))

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

        v_up = sum([resps[j][i]*pow(data[i] - t_mean,2)])
        v_down = m_down
        t_var = v_up/v_down
        res['variances'].append(t_var)

        res['pis'].append(1.0/nodists)

    return res

for i in range(iterations):
    resps = E_step(data,means,variances,pi)
    print(resps)
    nps = M_step(resps,data,dists)
    print(nps)
    means = nps['means']
    variances = nps['variances']
    pi = nps['pis']

print(pi)
print(means)
print(variances)
