
"""
This class executes ps.py for a predefined list of random numbers and
calculates the estimated mean response time for each run of the program.

For each random number in the list, ps.py simulates the ps server and produce
a csv file with running mean times for a defined number of jobs.
Then from this .csv file, the running mean response time is calculated 
"""

import ps
import scipy as sp
import scipy.stats
import numpy as np

print('Preprocessing...')
num_of_servers = 7 #the optimum number of switched on servers for minimum mean response time
#for s in range(3,11):
#   ps.executer(num_of_servers,90000,3)
#print('Preprocessing Completed')

'''
mean_confidence_interval(data, confidence=0.05) calculates the range of mean
response time for data, with the confidence interval of 95%
'''
def mean_confidence_interval(data, confidence=0.05):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h

random_seed = [1,5,25,34,88]
est_mean_response = []

print('Simulation running: {} servers switched on, for {} random seeds'.format(num_of_servers,len(random_seed)))
for seed in random_seed:
    ps.executer(num_of_servers,90000,seed)
    mean_res= ps.estimateMeanResponse('output-{}-{}.csv'.format(num_of_servers,seed),30000)
    est_mean_response.append(mean_res)


## Final result   
result = mean_confidence_interval(est_mean_response,confidence = 0.05)
print()
print('Mean response times for independant replications: ', est_mean_response)
print()
print('Mean response time is {} s in the range between {} and {} with a confidence interval of 95%'.format(result[0], result[1],result[2]))
