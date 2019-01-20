import sys
import math
import numpy as np
import pandas as pd
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------------------------------------
def get_histogram(min_val,max_val,no_bins,filename,values_list):
    bin_range = np.linspace(min_val,max_val,no_bins)
    freq, bin_edges = np.histogram(values_list,bin_range)
    print(bin_edges)
    print(freq)
    #freq, bin_edges = np.histogram(values_list,10)

    of1 = open(filename,'w')
    for i1 in range(0,len(freq)):
        of1.write('%f %f\n'%(bin_edges[i1]+(max_val-min_val)/(2*no_bins),freq[i1]*100/(len(values_list))))
    of1.close()
#____________________________________________________________________________________________________________
    


ifn1 = "rings_plane_distribution.dat"
input_lines = []
count = 0
with open(ifn1,'r') as if1:
    for line in if1:
        input_lines.append(line)


count = len(input_lines)
line1 = input_lines[0].split()
no_cols = len(line1)

data_values = []
for i1 in range(0,count):
    data_values.append([])

for i1 in range(0,count):
    line1.clear()
    line1 = input_lines[i1].split()
    for i2 in range(0,no_cols):
        data_values[i2].append(float(line1[i2]))

filenames = ['1.64_first_theta_histogram.dat','1.64_first_phi_histogram.dat']
hist_params = [[-3.15,3.15,20],[0,3.15,10]]

for i1 in range(0,2):
    get_histogram(hist_params[i1][0],hist_params[i1][1],hist_params[i1][2],filenames[i1],data_values[i1+1][:])
        
