import csv
import pandas as pd
import pickle as pkl

from numpy import nan
from paho.mqtt import client, publish
from os import system
from tabulate import tabulate
from time import sleep

from config import *
from shared import *

# Message Processing
# Callback function, invoked when a message is received
def on_message(client, userdata, message):
	topic = message.topic
	payload = message.payload.decode('UTF-8').split(',')
	global stat_matrix

	if 'dev' in message.topic:
		w = int(payload[1])
		D = int(payload[2])
		x = int(payload[3])
		y = int(payload[4])
		u = round(float(payload[5]), 4)
		dt1 = round(float(payload[6]), 2)
		dt2 = round(float(payload[7]), 2)
		dt3 = round(float(payload[8]), 2)
		
		z = int(payload[0])
		#stat_matrix.loc[z, 'z'] = int(payload[0])
		stat_matrix.loc[z, 'w'] = w
		stat_matrix.loc[z, 'D'] = D
		stat_matrix.loc[z, 'x'] = x
		stat_matrix.loc[z, 'y'] = y
		stat_matrix.loc[z, 'u'] = u
		stat_matrix.loc[z, 'Decision Time (Device)'] = dt1
		stat_matrix.loc[z, 'Decision Time (Gateway)'] = dt2
		stat_matrix.loc[z, 'Decision Time (Final)'] = dt3
		stat_matrix.loc[z, 'Decision Time (Total)'] = dt1 + dt2 + dt3
		stat_matrix.loc[z, 'Offloaded?'] = bool(x!=y and y != 0)
	elif 'cus' in message.topic:
		z = int(payload[0])
		et = float(payload[1])
		stat_matrix.loc[z, 'Execution Time'] = et
		stat_matrix.loc[z, 'Predicted Time'] = float(payload[2])
		stat_matrix.loc[z, 'Prediction Error'] = float(payload[3])
		stat_matrix.loc[z, 'Total Time'] = et + stat_matrix.at[z, 'Decision Time (Total)']
		stat_matrix.loc[z, 'Overdue?'] = bool(payload[4] == '1')
		if True not in pd.isna(stat_matrix).values and len(stat_matrix.index) == 8:
			publish.single('sgrm/spawn', '', qos=1, hostname=broker)
			
	
	elif 'fin' in message.topic:
		scenario = payload[0]
		overdue_total = stat_matrix['Overdue?'].sum()
		max_error = stat_matrix['Prediction Error'].abs().max()
		mean_error = stat_matrix['Prediction Error'].abs().mean()
		max_dt = stat_matrix['Decision Time (Total)'].max()
		mean_dt = stat_matrix['Decision Time (Total)'].mean()
		print(scenario + '\t: error max: ' + str(max_error) + ', mean: ' + str(mean_error))
		print('\t\t  Decision Time max: ' + str(max_dt) + ',  mean: ' + str(mean_dt))
		stat_matrix.to_csv(workdir + '/' + scenario + '.csv')
		stat_matrix = pd.DataFrame(columns=stat_matrix.columns)
		with open(workdir + '/stats.txt', 'a') as f:
			f.write(scenario + ': ' + str(overdue_total) + ' tasks overdue')
		
def on_connect(client, userdata, flags, rc):
	client.subscribe('sgrm/log/#')

stat_matrix = pd.DataFrame(columns=['z', 'w', 'D', 'x', 'y', 'u', 'Decision Time (Device)', 'Decision Time (Gateway)', 'Decision Time (Final)', 'Decision Time (Total)', 'Execution Time', 'Predicted Time', 'Prediction Error', 'Total Time', 'Overdue?', 'Offloaded?' ])
stat_matrix.set_index('z', inplace=True)

client = client.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, 1883, 60)

client.loop_start()

while True:
	sleep(1)
	system('clear')
	#print_logo('sgrm')
	print_logo('logger')
	print('')
	#if not stat_matrix.empty:
	#	stat_matrix = stat_matrix.sort_values('z')
	print(tabulate(stat_matrix, ['z', 'w', 'D', 'x', 'y', 'u', 'Decision Time\n(Device)', 'Decision Time\n(Gateway)', 'Decision Time\n(Final)', 'Decision Time\n(Total)', 'Execution Time', 'Predicted Time', 'Prediction Error', 'Total Time', 'Overdue?', 'Offloaded?'  ], tablefmt='presto'))
	print('')
	
