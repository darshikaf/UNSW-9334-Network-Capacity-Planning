from __future__ import division
import random
import math
import csv
import matplotlib.pyplot as plt
import numpy as np


class PS:
    def __init__(self):
        self.master_clock        = 0
        self.event_type          = None
        self.next_arrival_time   = 0
        self.next_departure_time = 0
        self.job_list            = []
        self.next_to_depart      = None
        self.orig                = {}
        
        
    def get_master_clock(self):
        return self.master_clock
    
    def set_master_clock(self,n):
        self.master_clock=float("%.10f"%n)
        
    def get_event_type(self):
        return self.event_type
    
    def set_event_type(self,n):
        self.event_type=n
        
    def get_next_arrival_time(self):
        return self.next_arrival_time
    
    def set_next_arrival_time(self,n):
        self.next_arrival_time = float("%.10f" % n)
        
    def get_next_departure_time(self): 
        if not self.job_list:
            self.next_to_depart =None
            return 9999
        min_service_time = min([x[1] for x in self.job_list])
        self.next_to_depart = [x for x in self.job_list if x[1] == min_service_time] 
        return len(self.job_list)*min_service_time
    
    def set_next_departure_time(self,n):
        self.next_departure_time = n
        
    def get_job_list(self):
        return self.job_list
    
    def set_job_list(self,etime,n):
        etime = float("%.10f" % etime)
        if  self.job_list:
            time_per_job  = float("%.10f" % (etime/len(self.job_list)))
            self.job_list = [(x[0],float("%.10f" % (x[1]-time_per_job))) for x in self.job_list]
        if n: 
            self.job_list.append(n)
            self.orig[n[0]] =n[1]
       # print self.job_list

    def remove_done_jobs(self):
        self.job_list = [x for x in self.job_list if x[0] not in [y[0] for y in self.next_to_depart] ]

def inter_arrival_times(n=None):
    if n:
        for _ in range(n):
            yield inter_arrival_time()
    else:
        while True:
            yield inter_arrival_time()

def inter_arrival_time():
    a1 = random.expovariate(7.2)
    a2 = random.uniform(0.75, 1.17)
    t = a1*a2
    return float("%.10f" % t)


def frequency_at_power_p(p):
    return (1.25 +0.31*(p/200-1))
   

def gen_service_time(s):
    power = 2000/s
    f=frequency_at_power_p(power)
    u=random.uniform(0, 1)
    t=10**(math.log10((u+8.174)/9.2)/0.14)
    return float("%.10f" % (t/f))

"""
estimateMeanresponse(filename,startpos) calculates the estimated mean
response time for the steady state component of each .csv file created
by executer(s,r,rseed)
startpos is the starting position of steady state for the given filename. startpos
is determined by visual inspection of the plots generated in transientRemoval.py
"""
def estimateMeanResponse(filename,startpos):
    lines=[]
    with open(filename) as f:
        lines = f.read().splitlines()
        nlines=lines[startpos:]
        return sum([float(x.split(',')[1]) for x in nlines])/len(nlines)

"""
executer(s,r,seed) simulates the ps server for r number of jobs when s number
of servers are switched on. rseed is the random seed.
The output is a .csv file which records the running mean response time for each
new job coming into the server.
"""
def executer(s,r,rseed):
    counter =0
    served_req = 0
    tot_res = 0
    ps =PS()
    k=0
    
    random.seed(rseed)
    
    outfile=open('output-%s-%s.csv' %(s,rseed),'w')
    output=csv.writer(outfile)
    output.writerow(['seq_no','mean_responce'])
    
    for i in inter_arrival_times(r*s):
        k += i
        if not (counter%s):
            last_cycle_time     = ps.get_master_clock()
            current_time        = ps.get_next_arrival_time()
            next_arrival        = current_time+k
            elapsed_time        = current_time-last_cycle_time
            #next_departure_time = ps.get_next_departure_time()
            ps.set_next_arrival_time(next_arrival)
            
            if not current_time:
                continue
            
            st = gen_service_time(s)
            ps.set_job_list(elapsed_time,( current_time,st)) 
            next_departure_time = current_time+ps.get_next_departure_time()

            while next_departure_time <= next_arrival:
                last_cycle_time = current_time
                current_time    = next_departure_time
                elapsed_time    = current_time-last_cycle_time
                tot_res += current_time-ps.next_to_depart[0][0]
                served_req += 1
                #print "NEXT" ,(tot_res/served_req),served_req,len(ps.get_job_list()), current_time-ps.next_to_depart[0][0],current_time,ps.next_to_depart 
                output.writerow([served_req,tot_res/served_req])
                ps.set_job_list(elapsed_time,None) 
                ps.remove_done_jobs()
                next_departure_time = current_time+ps.get_next_departure_time()
#               print "TT" , current_time,next_arrival,next_departure_time,elapsed_time, st
   #            print "JList" , ps.get_job_list()
            #print i, service_time(s)
            ps.set_master_clock(current_time)
            k=0
        counter += 1
    outfile.close()


