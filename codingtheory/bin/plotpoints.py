#!/usr/bin/env python
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

usage = """
Usage: ./pointshistogram.py [-no lim] [-np] [-out file] [-g points] infile

\tOptions:
\t\tno \t- No outliers. Removes all points that are more than LIM*SD from the mean of each variable.
\t\tnp \t- No points. This removes the scatterplot on top of the histogram.
\t\tout \t- Output file. This is the name of the file to save the 2d histogram. Must include extension.
\t\tg \t- Grid. This option is the number of points to use in the grid for the histogram.
\t\tinfile \t- Input file. This is the JSON file with a list of points.
"""

if len(sys.argv) < 2:
    print(usage)
    sys.exit(1)

argc = 1
no_outliers = False
if sys.argv[argc] == "-no":
    no_outliers = True
    argc+= 1
    ol = float(sys.argv[argc])
    argc+=1
    pass

plot_points = True
if sys.argv[argc] == "-np":
    plot_points = False
    argc += 1

outfile = None
if sys.argv[argc] == "-out":
    argc += 1
    outfile = sys.argv[argc]
    argc += 1
    pass

gpoints = 11
if sys.argv[argc] == "-g":
    argc += 1
    gpoints = int(sys.argv[argc])
    argc += 1
    pass

infile = sys.argv[argc]

f = open(infile)
points = json.load(f)
f.close()

x = [a[0] for a in points]
y = [a[1] for a in points]

sd_x = np.std(x)
m_x = np.mean(x)
sd_y = np.std(y)
m_y = np.mean(y)

print("Var\tMin\t\tMax\t\tMean\t\tSD\t\tElements")
print("X\t"+str(min(x))+"\t"+str(max(x))+"\t"+str(m_x)+"\t"+str(sd_x)+"\t"+str(len(x)))
print("Y\t"+str(min(y))+"\t"+str(max(y))+"\t"+str(m_y)+"\t"+str(sd_y)+"\t"+str(len(y)))

if no_outliers:
    print("Removing outliers")
    nw_x = [i for cnt,i in enumerate(x) if (m_x - ol*sd_x) <= i <= (m_x + ol*sd_x) and (m_y - ol*sd_y) <= y[cnt] <= (m_y + ol*sd_y)]
    nw_y = [i for cnt,i in enumerate(y) if (m_y - ol*sd_y) <= i <= (m_y + ol*sd_y) and  (m_x - ol*sd_x) <= x[cnt] <= (m_x + ol*sd_x)]

    x = nw_x
    y = nw_y
    sd_x = np.std(x)
    m_x = np.mean(x)
    sd_y = np.std(y)
    m_y = np.mean(y)

    print("New results")
    print("Var\tMin\t\tMax\t\tMean\t\tSD\t\tElements")
    print("X\t"+str(min(x))+"\t"+str(max(x))+"\t"+str(m_x)+"\t"+str(sd_x)+"\t"+str(len(x)))
    print("Y\t"+str(min(y))+"\t"+str(max(y))+"\t"+str(m_y)+"\t"+str(sd_y)+"\t"+str(len(y)))

gridx = np.linspace(min(x),max(x),gpoints)
gridy = np.linspace(min(y),max(y),gpoints)
grid, _, _ = np.histogram2d(x, y, bins=[gridx, gridy])

H, xedges, yedges = np.histogram2d(x, y, bins=[gridx, gridy])

H[H == 0] = 1
H_log = np.log(H)
H = H_log

fig = plt.figure()
myextent = [xedges[0],xedges[-1],yedges[0],yedges[-1]]
plt.imshow(H.T,origin='low',extent=myextent,interpolation='nearest',aspect='auto')
if plot_points: plt.plot(x, y, 'r*')
plt.colorbar()
plt.title("2D-Histogram of points in "+infile)
plt.xlabel("Heatmap in log scale. " + (str(ol)+"SD outliers excluded." if no_outliers else ""))
if outfile is None: plt.show()

if outfile is not None: fig.savefig(outfile)

c_x = [Ex - m_x for Ex in x]
c_y = [Ey - m_y for Ey in y]
Rx = np.cov(c_x,c_y)
print("Autocorrelation matrix: ")
print(Rx)
eigen = np.linalg.eig(Rx)
print("Eigenvalues: "+str(eigen[0]))
for i in range(len(eigen[1])):
    print("Eigenvector: "+str(eigen[1][i]))
