import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import csv

"""
This class is used to extract the steady state component from the running mean

From the plot generated in visualise.py, it was concluded that minimum mean
response time can be obtained when 7 servers are switched on. Also the no. of
jobs is determined as 90,000.
Therefore 7 servers and 90,000 jobs are used for this step.

A new .csv file is created to record the pairwise differences for the mean
response times for 7 servers. Then a plot is generated for the pairwise
differences against no. of jobs proessed. This plot illustrates the variations
in the mean response times. Then visual inspection is used to determine the
starting position of the steady sate.
"""

nlist=[]
seq=0
last_value=0
diff=0
outfile=open('output.csv','w')
output=csv.writer(outfile)
output.writerow(['seq_no','mean_responce'])
with open("output-7-3.csv") as f:
    for line in f:
        if 'seq_no' in line:
            continue
        s=line.rstrip().split(',')
        diff=abs(float(s[1])-float(last_value))
        output.writerow([s[0],diff])
        last_value=s[1]
        seq=s[0]        
    #lis=[line.split() for line in f]
    #for i,x in enumerate(lis):
    #        print ("line{0} = {1}".format(i,x))
print('Pairwise differences calculated')


##### Plotting the pairwise mean response time difference against no. of jobs###

per_data=genfromtxt('output.csv',delimiter=',',names=['x', 'y'])
y_min = -0.00025 #defines the scale of y axis
y_max = 0.0010 #defines the scale of y axis
no_of_jobs = 90000 #no_of_jobs processed

plt.axis([0, no_of_jobs, y_min, y_max])
plt.xlabel ('No. of jobs')
plt.ylabel ('Absolute value of pairwise difference in mean response time')
plt.title('Pairwise mean response time difference')
plt.plot(per_data['y'])

plt.show()
