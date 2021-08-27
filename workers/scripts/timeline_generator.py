# Generates a task timeline
import matplotlib.pyplot as plt
import pickle as pkl

from numpy.random import poisson
from random import gauss, randint
from scipy import stats
from sys import argv

task_deadlines = [ 18, 12, 3, 15 ]

# Helper function
def check_distribution(l, margin):
	for e in l:
		if e == 0:
			return False
		for i in range(len(l)):
			if abs((e - l[i]) / e) > margin:
				return False
	return True

num = int(input('Enter the number of tasks:'))
max_x = int(input('Enter the number of devices:'))
dist_name = input('Enter the name of the distribution [gauss, poisson]:')
mean = int(input('Enter the mean of the distribution:'))
if dist_name== 'gauss':
	stdev = int(input('Enter the standard deviation of the distribution:'))

flag = False
while not flag:
	apptypes = []
	apptypecnt = [0, 0, 0, 0]
	for i in range(num):
		w = randint(0, 3)
		apptypes.append(w)
		apptypecnt[w] += 1
	flag = check_distribution(apptypecnt, 0.1)
	
plt.bar(['Deepspeech', 'Facenet', 'Lanenet', 'Retain'], apptypecnt)
plt.plot()
plt.show()

flag = False
while not flag:
	appdevices = []
	appdevicecnt = [0 for i in range(max_x)]
	for i in range(num):
		x = randint(1, max_x)
		appdevices.append(x)
		appdevicecnt[x-1] += 1
	flag = check_distribution(appdevicecnt, 1)

plt.bar(list(range(1, max_x + 1)), appdevicecnt[0:max_x])
plt.plot()
plt.show()

name = ''
while not name:
	apptimes = []
	timeline = []
	for i in range(num):
		t = -1
		while t < 0 or t > mean + stdev:
			if dist_name == 'gauss':
				t = gauss(mean, stdev)
			elif dist_name == 'poisson':
				t = poisson(mean)
		task = [ i, t, apptypes[i], appdevices[i], task_deadlines[apptypes[i]] ]
		apptimes.append(t)
		timeline.append(task)
	
	plt.hist(apptimes, bins=6)
	plt.plot()
	plt.show()

	name = input('Name the distribution (leave blank to recreate): ')

with open(name + '.pkl', 'wb') as f:
	pkl.dump(timeline, f)
	
