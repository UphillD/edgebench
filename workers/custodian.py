# Edgebench Platform
# Worker Scripts
# Custodian Module
#
# Starts, monitors and maintains a combination of applications
#
# Data Structures:
#     task_matrix: [ 'z', 'w', 'D', 'Start Timestamp', 'Estimated Duration' ]
#         Stores information for tasks currently running
#         Pandas DataFrame
#         Types:   [ int, int, int, flt, flt ]
#
#     state_matrix: [ 'ID', 'App', 'State', 'z' ]
#         Stores information for the state of machine instances
#         Pandas DataFrame
#         Types:   [ int, str, str, int ]

import pandas as pd
import pickle as pkl

from glob import glob
from os import chdir, path, remove, system
from paho.mqtt import publish
from shutil import copy
from subprocess import Popen, DEVNULL
from sys import argv
from tabulate import tabulate
from time import sleep, time

from config import *
from shared import *

# Print help message
if len(argv) == 1:
	print('Not enough arguments!')
	print('')
	print('Usage: python3 custodian.py <platform> <app combo>')
	print('           where <app combo> is the number of instances')
	print('           of every app, in the form of a,b,c,d')
	print('')



# Initializer & Subscriber
# args: custodian.py <app combo> <platform>
elif len(argv) == 3:

	# Grab the platform & set the app profile
	platform = argv[1]
	# Grab the application a,b,c,d combination, turn it into a list
	combo = list(map(int, argv[2].split(',')))

	# Initialize the task matrix & store it
	remove_matrix(workdir + '/task_matrix.pkl')
	task_matrix = pd.DataFrame(columns=['z', 'w', 'D', 'Start Timestamp', 'Estimated Duration'])
	task_matrix.set_index('z', inplace=True)
	write_matrix(task_matrix, workdir + '/task_matrix.pkl')

	# Initialize the state matrix & store it too
	state_matrix = pd.DataFrame(columns=['ID', 'App', 'State', 'z'])
	state_matrix.set_index('ID', inplace=True)
	state_matrix = state_matrix.astype(str)
	remove_matrix(workdir + '/state_matrix.pkl')

	# Delete any leftover queue files
	for f in glob(workdir + '/*.que'):
		remove(f)

	# Switch to the root edgebench folder to properly launch the docker images
	chdir(rootdir)
	# Launch the docker images
	k = 1
	# Loop through the 4 applications
	for i in range(0, 4):
		# Loop through the number of instances for each application
		for j in range(combo[i]):
			# Launch the docker image through a python subprocess
			Popen(['./entrypoint.sh', platform, 'listen', apps[i], str(k)], stdout=DEVNULL)
			# Add a new entry in the state matrix
			state_matrix.loc[k] = [ apps[i], 'idle', 0 ]
			k += 1

	# Switch back to the working directory
	chdir(workdir)
	write_matrix(state_matrix, workdir + '/state_matrix.pkl')


	# Use generator function for progress bar (see shared.py)
	stage = 0	# progress bar stage
	gen = print_progress_bar()

	# inf loop, exit with CTRL + C
	while True:
		# Print logos, matrices and other information
		sleep(0.1)
		system('clear')
		print_logo('edgebench')
		print_logo('custodian', -1, 'PURPLE')
		print('')
		print('')
		print('\t   ⚒   TASKS   ⚒')
		print('')
		print(tabulate(task_matrix.drop(['Start Timestamp', 'Estimated Duration'], 1), ['z', 'App'], tablefmt='fancy_grid'))
		print('')
		print('')
		print('\t   ⛯   STATES   ⛯')
		print('')
		print(tabulate(state_matrix, ['ID', 'App', 'State', 'z'], tablefmt='fancy_grid'))
		print('')
		print('')
		next(gen)
		print('')

		###
		# Check 1 : Completed tasks
		# Look through every machine instance
		for index, row in state_matrix.iterrows():
			# Check if instance is labeled as running, but the indicator file is gone
			if row['State'] == 'running' and not path.isfile(workdir + '/app_' + str(index) + '/exec.tmp'):
				
				# Grab finish timestamp
				et = round(time(), 3)
				# Get ID of task
				z = row['z']
				
				# Update the state matrix
				state_matrix.at[index, 'State'] = 'idle'
				state_matrix.at[index, 'z'] = 0
				write_matrix(state_matrix, workdir + '/state_matrix.pkl')

				# Drop the task row from the task matrix
				task_matrix = read_matrix(workdir + '/task_matrix.pkl')
				st = task_matrix.loc[z, 'Start Timestamp']
				pd = task_matrix.loc[z, 'Estimated Duration']
				task_matrix.drop(z, axis=0, inplace=True)				
				
				current_tasks = len(task_matrix)
				tasks_weighted = []
				for i in range(4):
					tasks_weighted.append(sum_mask_numpy(task_matrix, i))
					
				# Update the rest of the tasks
				for index_tm, row_tm in task_matrix.iterrows():
					w_tm = row_tm['w']
					
					# Calculate times
					done_t = time() - row_tm['Start Timestamp']
					total_t = row_tm['Estimated Duration']
					remaining_per = 1 - ( done_t / total_t )
					
					# Calculate remaining time and total predicted duration
					remaining_t = calculate_time(w, current_tasks, tasks_weighted, remaining_per)
					duration = done_t + remaining_t
					
					task_matrix.at[index_tm, 'Estimated Duration'] = duration
				
				write_matrix(task_matrix, workdir + '/task_matrix.pkl')

				# Log 5: execution
				payload = make_payload(z, st, et, pd)
				publish.single('edgebench/log/execution', payload, qos=1, hostname=broker)

		###
		# Check 2 : New tasks
		# Look through every .que file in workdir
		new_tasks = glob('*.que')
		if len(new_tasks) > 0:
			# Create new_task list with task information
			new_task = new_tasks[0][:-4].split(',')
			# Grab task information
			z = int(new_task[0])
			w = int(new_task[1])
			D = int(new_task[2])

			# Check state matrix to find available machine instance
			for index, row in state_matrix.iterrows():
				if row['App'] == apps[w] and row['State'] == 'idle':
					task_matrix = read_matrix(workdir + '/task_matrix.pkl')

					# Delete .que file
					remove(new_tasks[0])
					
					
					current_tasks = len(task_matrix)
					tasks_weighted = []
					for i in range(4):
						tasks_weighted.append(sum_mask_numpy(task_matrix, i))
					tasks_weighted[w] = tasks_weighted[w] + 1
					
					# Update the rest of the tasks
					for index_tm, row_tm in task_matrix.iterrows():
						w_tm = row_tm['w']
						
						# Calculate times
						done_t = time() - row_tm['Start Timestamp']
						total_t = row_tm['Estimated Duration']
						remaining_per = 1 + ( done_t / total_t )
						
						# Calculate remaining time and total predicted duration
						remaining_t = calculate_time(int(w_tm), current_tasks + 1, tasks_weighted, remaining_per)
						duration = round(done_t + remaining_t, 2)
						
						task_matrix.at[index_tm, 'Estimated Duration'] = duration
					
					# Calculate predicted duration
					duration = calculate_time(w, current_tasks + 1, tasks_weighted)
					# Add new row with new task information in task_matrix
					st = round(time(), 3)
					task_matrix.loc[z] = [ w, D, st, duration ]
					write_matrix(task_matrix, workdir + '/task_matrix.pkl')

					task_name, task_payload = categorize_task(w)

					# Start the task
					state_matrix.at[index, 'State'] = 'running'
					state_matrix.at[index, 'z'] = z
					write_matrix(state_matrix, workdir + '/state_matrix.pkl')
					machine = index
					copy(payloaddir + '/' + task_name + '/' + task_payload, workdir + '/app_' + str(machine) + '/' + task_payload)

					break

