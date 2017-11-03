# -*- coding: utf-8 -*-

__author__ = "Zafeirios Fountas"
__credits__ = ["Murray Shanahan", "Mark Humphries",  "Rob Leech", "Jeanette Hellgren Kotaleski"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Zafeirios Fountas"
__email__ = "fountas@outlook.com"
__status__ = "Published"

from brian import *
from numpy import cos, pi
from os import path

def fitnessFunction(inhA, inhB, notInh, PRINT=True) :
    inhA = float(inhA) # Nimber of spikes in the first inhibited channel
    inhB = float(inhB) # Nimber of spikes in the first inhibited channel
    notInh = float(notInh) # Nimber of spikes in the free channel

    allSpikes = inhA + inhB + notInh

    if allSpikes == 0 :
        print "No spikes reported here - Score is 0"
        return 0.0

    # The percentage of spikes in the channels that are supposed to receive them
    inhPercentage = (inhA + inhB) / allSpikes   # Between [0,1]

    if (inhA+inhB) == 0 :
        print "No spikes in the inhibited areas reported here - Score is 0"
        return 0.0
    perA = inhA/(inhA+inhB)


    if perA > 0.5 :
        perA = 1.0 - perA

    closenessOfAandB = 2.0*perA # Between [0,1]

    score = (inhPercentage**7.0)*closenessOfAandB

    if PRINT :
        print '\t\tScore:', score,"  \t(inhA:",inhA,"inhB:",inhB,"notInh",notInh,")"
        print '\t\t\tinh:      ',inhPercentage,"\t(against:",(1.0-inhPercentage),")"
        print '\t\t\tCloseness:',closenessOfAandB, "\t(perA", perA,")"

    return score


def HIGH_FREQ(t, freq) :
    if freq == 0.0 :
        return 1.0
    else:
        return (1.0+cos( freq*2.0*pi*t ))

# I implement a random walk with boundaries LOW and HIGH and in order to feed 
# the returned list to the function in the rate argument of the PoissonGroup
def RandWalkList(LOW, HIGH, duration=50000) :
    Y = []
    Nsigma = 0.5 # 1.0
    Nmean = -0.05 # NOTE: A bit negative so there is only small portion of short higly active inputs.
    HIGH = float(HIGH)
    LOW = float(LOW)
    mean = (HIGH-LOW)/2.0
    my_list = list(np.random.normal(Nmean, Nsigma, duration))
    for i in range(duration) :
        mean = mean + my_list[i]
        if mean > 10.0 : mean = 10.0
        if mean < 0.0 : mean = 0.0
        Y.append(mean)
    return Y

def ListRates(t, input_list=[]) :
    return input_list[int(t*1000.0)]*Hz

def RampRates(t, start, end, ramp_dur, base, freqLOW, freqHIGH, phaseLOW, Tamp) :
    if t > start and t < end :
        if float(freqLOW) == 0.0 :
            oscillation = Tamp
        else :
            oscillation = (1.0+cos( freqLOW*2.0*pi*t + phaseLOW * second))*HIGH_FREQ(t,freqHIGH)*Tamp
        # Activate the ramp (from 0 to 1)
        if t < start + ramp_dur : # Angle is 1/dur
            return base + oscillation * float(t-start)/float(ramp_dur)
        else :
            return base + oscillation
    else :
        return 3.0*Hz

def T1rates_tr(t, start, end, base, freqLOW, freqHIGH, T1_amp) :
    if t > start and t < end :
        if float(freqLOW) == 0.0 :
            return base + T1_amp
        else :
            return base + (1.0+cos( freqLOW*2.0*pi*t ))*HIGH_FREQ(t,freqHIGH)*T1_amp
    else :
        return 3.0*Hz

def T2rates_tr(t, start, end, base, freqLOW, freqHIGH, phaseLOW, T2_amp) :
    if t > start and t < end :
        if float(freqLOW) == 0.0 :
            return base + T2_amp
        else :
            return base + (1.0+cos( freqLOW*2.0*pi*t + phaseLOW * second))*HIGH_FREQ(t,freqHIGH)*T2_amp
    else :
        return 3.0*Hz

def T1rates(t, base, freqLOW, freqHIGH, T1_amp) :
    return base + (1.0+cos( freqLOW*2.0*pi*t ))*HIGH_FREQ(t,freqHIGH)*T1_amp
    #return (1.0+cos( freqLOW*2.0*pi*t ))*HIGH_FREQ(t,freqHIGH)*T1_amp

def T2rates(t, base, freqLOW, freqHIGH, phaseLOW, T2_amp) :
    return base + (1.0+cos( freqLOW*2.0*pi*t + phaseLOW * second))*HIGH_FREQ(t,freqHIGH)*T2_amp
    #if t > 300*ms :
    #    return base + (1.0+cos( freqLOW*2.0*pi*t + phaseLOW * second))*HIGH_FREQ(t,freqHIGH)*T2_amp
    #else :
    #    return base
    #return (1.0+cos( freqLOW*2.0*pi*t + phaseLOW * second))*HIGH_FREQ(t,freqHIGH)*T2_amp



def post_progress(progress, slotX, slotY, exp_name, message="") :
    from pycurl import Curl
    import cStringIO
    from socket import gethostname
    response = cStringIO.StringIO()
    address ='www.doc.ic.ac.uk/~zf509/'+exp_name+'/ip.php?name='+gethostname()+\
             '-'+message+'&slot='+str(slotX)+'-'+str(slotY)+\
             '&stage='+str(progress)
    c = Curl()
    c.setopt(c.WRITEFUNCTION, response.write)
    c.setopt(c.URL, address)
    c.perform()
    c.close()
    server_res = response.getvalue()
    
    print "Server replied:", server_res
    if server_res[0]=="T" and server_res[1]=="E" and server_res[2]=="R" :
        return False
    else :
        return True



# Used in STN model!
def IMP(u, imp) :# abs could be ommited if I make sure that the sign is correct!
    return (1.0/(imp * abs(u) + 1.0/imp))
def izhi_reset_stn(P, spikes) :
    P.v[spikes] = P.c[spikes] - (IMP(P.u2[spikes],P.w1[spikes]) * P.u2[spikes])*ms
    #P.v[spikes] = P.c[spikes] - P.u2_imp[spikes] * P.u2[spikes]*ms
    P.u1[spikes] += P.d1[spikes]
    P.u2[spikes] += P.d2[spikes]

# It's already vectorized!!
def heaviside(x):
    x = np.array(x)
    if x.shape != ():
        y = np.zeros(x.shape)
        y[x > 0.0] = 1
        y[x == 0.0] = 0.5
    else: # special case for 0d array (a number)
        if x > 0: y = 1
        elif x == 0: y = 0.5
        else: y = 0
    return y

# It's already vectorized!!
# It returns zero, if x < 0 and 1 otherwise..
def heaviside01(x):
    x = np.array(x)
    if x.shape != ():
        y = np.zeros(x.shape)
        y[x >= 0.0] = 1.0
    else: # special case for 0d array (a number)
        if x >= 0: y = 1.0
        else: y = 0.0
    return y


# Used to populate the neuron arrays with different parameters
from numpy.random import rand
import numpy as np

def two_choices(size, prob1, choice1, choice2) :
    result = []
    for i in rand(size) :
        if i < prob1 :
            result.append(choice1)
        else :
            result.append(choice2)
    return np.array(result)


def three_choices(size, prob1, prob2, choice1, choice2, choice3) :
    result = []
    for i in rand(size) :
        if i < prob1 :
            result.append(choice1)
        elif i < (prob1+prob2) :
            result.append(choice2)
        else :
            result.append(choice3)
    return np.array(result)

def two_det_choices(size, channels, prob1, choice1, choice2) :
    result = []
    channel_size = int(size/channels)
    first  = int(round(channel_size*prob1))
    second  = channel_size - first
    for i in range(channels) :
        for j in range(first) :
            result.append(choice1)
        for j in range(second) :
            result.append(choice2)
    return np.array(result)

def three_det_choices(size, channels, prob1, prob2, choice1, choice2, choice3) :
    result = []
    channel_size = int(size/channels)
    first  = int(round(channel_size*prob1))
    second = int(round(channel_size*prob2))
    third  = channel_size - first - second
    for i in range(channels) :
        for j in range(first) :
            result.append(choice1)
        for j in range(second) :
            result.append(choice2)
        for j in range(third) :
            result.append(choice3)
    return np.array(result)

# Used to populate C with a suggested SD adding a limit (0.5*C) and resampling
# import numpy as np
def get_random_C(C, C_var, N, mySeed) :
    #np.random.seed(seed = mySeed)
    C_list = np.random.normal(C, C_var, N)
    for i in range(N) :
        while abs(C_list[i] - C) > 0.5 * C :
            C_list[i] = np.random.normal(C, C_var, 1)
    return C_list

# Returns a list where the first element is the general firing rate and the next
# N elements are the firing rates of each individual channel (of a total N)
# duration: duration of simulation
def calc_firing_rates(spikes_data, neurons_per_ch, duration = 1.0):
    ch = []
    channels = len(spikes_data)
    ch.append(0.0)
    for i in range(channels) :
        ch.append( round( spikes_data[i]/(float(neurons_per_ch*duration)), 2) )
    ch[0] = round(sum(ch)/channels,2)
    return ch








