# edgebench/algo/config.py
# Configuration file
import pandas as pd
from math import log, inf
from time import time

from shared import *

# Settings
broker = '147.102.37.162'		# Broker IP
device_name = 'amd64'				# device name, automatically edited by prepare script
transfer_speed = 150000			# Transfer Speed (BPS)
reward_table = [ 1, 1, 1, 1 ]	# Reward Table for payoff function

# Directories
rootdir    = '/app'
workdir    = rootdir + '/data/workdir'
payloaddir = rootdir + '/data/payloads'
algodir    = rootdir + '/algo'

# task profile table
#					[ chunks,   a   ,   b   , wt(1), wt(2), wt(3), wt(4) ]
task_profiles = {
	'rpi4'		: [ [  7.809, -0.167,  0.704, 1.537, 1.760, 1.493, 1.203 ],
					[  3.081,  0.185, -0.176, 2.165, 1.501, 1.708, 1.240 ],
					[  1.410, -0.203,  0.870, 1.347, 1.253, 1.521, 1.068 ],
					[  9.718, -0.455,  1.303, 1.095, 1.482, 1.595, 1.355 ] ],
	'rpi4_2'	: [ [  8.667, -0.003,  0.569, 1.452, 1.800, 1.549, 1.209 ],
					[  3.714,  0.332, -0.139, 1.796, 1.496, 1.549, 1.246 ],
					[  1.365,  0.055,  0.658, 1.348, 1.315, 1.565, 1.125 ],
					[  9.837, -0.233,  1.086, 1.089, 1.488, 1.628, 1.395 ] ],
	'rpi4_3'	: [ [  8.679, -0.031,  0.607, 1.454, 1.780, 1.540, 1.158 ],
					[  3.909,  0.350, -0.118, 1.729, 1.459, 1.577, 1.222 ],
					[  1.628, -0.008,  0.683, 1.395, 1.322, 1.605, 1.124 ],
					[  9.948, -0.332,  1.192, 1.089, 1.513, 1.663, 1.371 ] ],	
	'tegra'		: [ [  6.723,  0.103,  0.449, 1.416, 1.589, 1.426, 1.266 ],
					[  2.327,  0.467, -0.397, 1.805, 1.457, 1.481, 1.274 ],
					[  0.965,  0.267,  0.418, 1.296, 1.288, 1.400, 1.136 ],
					[  9.290, -0.135,  1.159, 1.073, 1.310, 1.313, 1.198 ] ],
	'nano'		: [ [  8.096, -0.042,  0.713, 1.409, 1.500, 1.347, 1.236 ],
					[  3.166,  0.158,  0.188, 1.662, 1.446, 1.467, 1.261 ],
					[  1.112, -0.014,  0.787, 1.303, 1.297, 1.407, 1.152 ],
					[ 12.076, -0.465,  1.643, 1.055, 1.267, 1.262, 1.152 ] ],
	'amd64'		: [ [  6.918,  1.913, -0.394, 1.051, 1.118, 1.059, 1.004 ],
					[  0.949,  2.068, -0.794, 1.096, 1.135, 1.115, 1.038 ],
					[  0.390,  2.735, -1.085, 1.025, 1.050, 1.025, 1.025 ],
					[  2.831,  1.994, -0.585, 1.017, 1.163, 1.181, 1.052 ] ],
	'amd64_2'	: [ [  8.845, -0.514,  1.287, 1.085, 1.280, 1.120, 0.981 ],
					[  1.485,  0.058,  0.594, 1.414, 1.200, 1.290, 1.152 ],
					[  0.496, -0.169,  0.828, 1.270, 1.143, 1.429, 1.127 ],
					[  4.967, -0.491,  1.429, 0.962, 1.002, 1.303, 1.077 ] ]
}
profile = task_profiles[device_name]	# Set profile from device_name

# Functions
# Time prediction function
def calculate_time(w, current_tasks, task_table, remaining_per=1):
	
	chunks  = profile[w][0]
	a       = profile[w][1]
	b       = profile[w][2]
	weights = profile[w][3:]
	
	task_count_wtd = 0
	for i in range(4):
		task_count_wtd += task_table[i] * weights[i]
	
	# Estimate compensation function
	task_count = sum(task_table)
	if task_count == 1:
		compf = 0
	else:
		compf = a * log(task_count_wtd) + b
		
	# Predict time
	pred_t = ( chunks * task_count_wtd) / (1 + compf)
	
	return pred_t * remaining_per
	
# spawn_task function
# Receives task information as input
# Generates the appropriate .que file
def spawn_task(z, w, D, st):
	queue_file = str(z) + ',' + str(w) + ',' + str(D) + ',' + str(st) + '.que'
	queue_path = workdir + '/' + queue_file
	Path(queue_path).touch()

# Payoff function
def calculate_payoff(z, w, D, tt=0.0):

	# Initialize overdue counter
	overdue = 0
	# Open & load task matrix
	task_matrix = read_matrix(workdir + '/task_matrix.pkl')
	
	# recalculate execution times with +1 task
	current_tasks = len(task_matrix) + 1
	tasks_weighted = []
	for i in range(4):
		tasks_weighted.append(sum_mask_numpy(task_matrix, i))
	tasks_weighted[w] = tasks_weighted[w] + 1
	
	for index, row in task_matrix.iterrows():
		Dt = float(row['D'])
		if row['Projected Duration'] < Dt:
			elapsed_time = time() - row['Start Timestamp']
			wt = row['w']
						
			# Calculate times
			done_t = time() - row['Start Timestamp']
			total_t = row['Projected Duration']
			remaining_per = 1 - ( done_t / total_t )
			
			remaining_t = calculate_time(int(wt), current_tasks, tasks_weighted, remaining_per)
			duration = done_t + remaining_t
			
			if duration > Dt:
				overdue += 1
		
	state_matrix = read_matrix(workdir + '/state_matrix.pkl')
	wt = inf
	# Estimate waiting time
	for index, row in state_matrix.iterrows():
		if row['App'] == apps[w]:
			if row['State'] == 'idle':
				wt = 0.0
				break
			else:
				nt = task_matrix.at[row['z'], 'Projected Duration'] * 1.2	# 20% Error Margin
				if nt < wt:
					wt = max(nt - tt, 0.0)
	
	acet = calculate_time(w, current_tasks, tasks_weighted)

	# Final calculations
	# Penalty function
	penalty = D / ( D - tt - wt - acet )
	
	# Task penalty function
	t_penalty = 1
	for i in range(current_tasks): t_penalty *= 1.1
	
	# Deadline tuner
	tuner = 2
	for i in range(overdue) : tuner *= 0.6
	if acet >= D            : tuner *= 0.6
	
	# QoS tuner
	reward = reward_table[w]
	
	# Payoff function
	payoff = ( reward * tuner ) / ( penalty  * t_penalty )
	
	return payoff
