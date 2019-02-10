import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import ps


"""
This class visualises the variation of mean response time against the
number of jobs sent to the server.

The plot generated is used to determine the number of switched on servers
that results in minimum mean response time
"""


random_seed=3
no_of_jobs = 90000 #defines the number of jobs processed
print('Simulation started')
for s in range(3,11): #the number of servers switched on
   ps.executer(s,no_of_jobs,random_seed) 
print('Simulation Completed')
print('Waiting for the plot...')


##### Plotting the running mean response time for each server ####
for i in range(3,11):
    per_data=genfromtxt('output-{}-{}.csv'.format(i,random_seed),delimiter=',',names=['x', 'y'])
    plt.xlabel ('No. of jobs')
    plt.ylabel ('Mean response time')
    plt.title('Mean response times for 90,000 jobs')
    plt.plot(per_data['y'], label='$ Active Servers-%i.csv$' % i)
    plt.legend()
plt.show()




