import numpy as np

import matplotlib.pyplot as plt

from Models import *

def print_params(par, fname):
	eventID = 0
	with open(fname,"w+") as f:
		f.write("eventID, Amplitude, Duration, Model\n")
		for i in range(len(par)):
			f.write("{}, {}, {}, B \n".format(i, par[i]['amplitude'], par[i]['duration']))
			eventID += 1
	return 0






# Time stamps [s] of observations (assume common to all events)
times = np.linspace(-50, 50, 101)


# Number of events in catalog
Nevents = 10


# Generate random parameters for each event
#
# Amplitude log-normally distributed around 1 with unit width
# Duration normally distributed around 10s with width 1s 
#
event_params = [ 
                {'amplitude': np.random.lognormal(mean=0.0, sigma=1.0), 'duration': np.random.normal(10, 1)}
        for N in range(Nevents) ]
print_params(event_params, 'data/event_params.txt')


# Generate mock signals: modelB + noise
sigma = 0.1
catalog = np.zeros((len(times), Nevents+1))
catalog[:,0] = times
for N in range(Nevents):
    catalog[:,N+1] = ModelB_lightcurve(times, event_params[N]) + np.random.normal(0, sigma, size=len(times))


# Plot mock signals in catalog
for N in range(Nevents):
    plt.plot(times, catalog[:,N+1])
    
plt.xlabel("Time / s")
plt.ylabel("Flux")
plt.show()


# Export catalog
head = "\n# The 1 sigma error on all flux measurements is {}\n\n".format(sigma)
head += "# Time [s], "
for N in range(Nevents):
    head += "Flux event "+str(N)+", "
head = head[0:-2]
np.savetxt("data/catalog.dat", catalog, header=head, fmt='%.5e')
