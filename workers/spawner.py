# Edgebench Platform
# Worker Scripts
# Spawner Module
#
# Usages: python3 spawner <command>
#     commands: oracle <timeline> <# of offload targets>
#               timeline <timeline> <# of devices> <# of gateways>

import pickle as pkl

from paho.mqtt import publish, subscribe
from time import sleep, time
from os import system
from pathlib import Path
from random import gauss, randint
from sys import argv

from config import *
from shared import *

def task_generator(n):
	timeline = []
	for i in range(1, n + 1):
		t = -1
		z = i
		while (t < 0):
			t = gauss(10, 5)
		w = randint(0, 3)
		x = randint(1, 1)
		D = task_deadlines[w]

		task = [ z, t, w, x, D ]
		timeline.append(task)

	return timeline

def increment_list(l):
	l[0] += 1
	if l[0] > 2:
		l[0] = 0
		l = [ l[0] ] + increment_list(l[1:])
	return l

clk = 0.0
system('clear')
print_logo('edgebench')
print_logo('spawner', -1, 'PURPLE')
print('')

if argv[1] == 'timeline':
	with open(tmldir + '/' + argv[2] + '.pkl', 'rb') as f:
		timeline = pkl.load(f)
	timeline.sort(key=lambda x: x[1])

	for element in timeline:
			z = element[0]
			t = element[1]
			w = element[2]
			x = element[3]
			D = element[4]

			# wait for next task
			sleep(t - clk)
			clk = t

			#(z, w, x, Ω, st)
			# publish next task
			# https://pypi.org/project/paho-mqtt/#id3
			print('Spawning task ({}, {}, {}) on device {}'.format(z, w, D, x))
			payload = make_payload(z, w, D, x)
			publish.single('edgebench/device/spawn/' + str(x), payload, qos=1, hostname=broker)

			st = round(time(), 3)
			payload = make_payload(z, w, D, x, st)
			publish.single('edgebench/log/spawn', payload, qos=1, hostname=broker)

	#payload = input("Enter the name of the final log:")
	#publish.single('edgebench/log/complete', payload, qos=1, hostname=broker)

elif argv[1] == 'oracle':

	Y = int(argv[3])

	with open(tmldir + '/' + argv[2] + '.pkl', 'rb') as f:
		timeline = pkl.load(f)
	timeline.sort(key=lambda x: x[1])

	offload = [ 0, 0, 0, 0, 0, 0, 0, 0 ]

	for i in range((Y + 2) ** len(offload)):
		clk = 0.0

		for index, element in enumerate(timeline):
			z = element[0]
			t = element[1]
			w = element[2]
			x = element[3]
			D = element[4]

			sleep(t - clk)
			clk = t

			y = offload[index]


			payload = make_payload(z, w, D, x, y)
			#print('Spawning task ({}, {}, {}) on device {}, will be offloaded to {}'.format(z, w, D, x, y))
			publish.single('edgebench/device/spawn/' + str(x), payload, qos=1, hostname=broker)

		#subscribe.simple('edgebench/spawn', qos=1, hostname=broker)

		#sleep(5)
		#payload = 'Oracle_' + str(i)
		#publish.single('sgrm/log/fin', payload, qos=1, hostname=broker)
		offload = increment_list(offload)
		print(offload)
		sleep(2)


else:
	timeline = task_generator(int(argv[1]))
	timeline.sort(key=lambda x: x[1])

	for element in timeline:

		# wait for next task
		sleep(element[1] - clk)
		clk = element[1]

		z = int(element[0])
		w = int(element[2])
		D = int(element[4])
		x = int(element[3])

		#(z, w, x, Ω)
		#st = str(round(time(), 2))
		#payload = str(element[0]) + ',' + str(element[2]) + ',' + str(element[4]) + ',' + str(element[3])# + ',' + st
		payload = make_payload(z, w, D, x)
		# publish next task
		# https://pypi.org/project/paho-mqtt/#id3
		print('Spawning task ({}, {}, {}) on device {}'.format(element[0], element[2], element[4], element[3]))
		publish.single('edgebench/device/spawn/' + str(element[3]), payload, qos=1, hostname=broker)
		st = round(time(), 3)

		payload = make_payload(z, w, D, x, st)
		publish.single('edgebench/log/spawn', payload, qos=1, hostname=broker)



	payload = input("Enter the name of the final log:")
	publish.single('edgebench/log/save', payload, qos=1, hostname=broker)
