#!/bin/python3
# Edgebench Framework
# sysmon Module
# 
# General Functionality

from os import system
from subprocess import Popen, PIPE, DEVNULL
from sys import argv

# Launches a monitor instance
def sysmonitor():
	cmd = [ 'sar', '-ur', '-P ALL', '1', '-o syslog.bin']
	PID = Popen(cmd, stdout=DEVNULL, stderr=DEVNULL)
	return(PID)

# Kills a launched monitor instance
def syskill(PID):
	from os import kill
	from signal import SIGTERM
	kill(int(PID), SIGTERM)

# Generates a report
def sysreport():
	import pandas as pd
	from multiprocess import cpu_count
	# Create columns for resulting dataframe
	cores = cpu_count()
	cols_info = [ 'hostname', 'interval', 'timestamp']
	cols_mem = [ 'kbmemfree', 'kbavail', 'kbmemused', '%memused', 'kbbuffers', 'kbcached', 'kbcommit', '%commit', 'kbactive', 'kbinact', 'kbdirty' ]
	cols_cpu = [ 'CPU_all', '%user_all', '%nice_all', '%system_all', '%iowait_all', '%steal_all', '%idle_all' ]
	for i in range(cores):
		cols_cpu = cols_cpu + [ 'CPU_'+str(i), '%user_'+str(i), '%nice_'+str(i), '%system_'+str(i), '%iowait_'+str(i), '%steal_'+str(i), '%idle_'+str(i) ]
	cols = cols_info + cols_cpu + cols_mem
	
	proc = Popen('./sysreport.sh', stdout=PIPE)
	output = '\n'.join(proc.stdout.read().decode('utf-8').split('\n')[1:])
	with open('syslog.csv', 'w') as fd:
		fd.write(output)
	df = pd.read_csv('syslog.csv', sep=';', header=None, names=cols)
	df = df.drop(['hostname', 'interval', 'CPU_all'], axis=1)
	for i in range(cores):
		df = df.drop(['CPU_'+str(i)], axis=1)
	df = df.tail(10)

	return(df)
	
if __name__ == '__main__':
	if argv[1] == 'monitor':
		res = sysmonitor().pid
	elif argv[1] == 'kill':
		try:
			syskill(int(argv[2]))
		except IndexError:
			print('No PID provided')
	elif argv[1] == 'report':
		df = sysreport()
