# Edgebench Platform
# Worker Scripts
# Logger Module
#
# Logs:
#     ┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
#     |     SGRM     |     DMRM     | Offload None | Offload  All |    Oracle    |
# ┌───┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
# | 0 | Register (g) | Register (d) |     ----     |     ----     |     ----     |
# | 1 | Spawn    (s) | Spawn    (s) | Spawn    (s) | Spawn    (s) | Spawn    (s) |
# | 2 | Auction  (d) | Auction  (d) |     ----     |     ----     |     ----     |
# | 3 | Bid      (g) | Decide   (g) |     ----     |     ----     |     ----     |
# | 4 | BidFirst (g) |     ----     |     ----     |     ----     |     ----     |
# | 5 | Offload  (d) | Offload  (d) |     ----     | Offload  (d) | Offload  (d) |
# | 6 | Execute  (c) | Execute  (c) | Execute  (c) | Execute  (c) | Execute  (c) |
# └───┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
#
#        where: s -> spawner
#               d -> device
#               g -> gateway
#               c -> custodian

import pandas as pd

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
	payload = message.payload.decode('UTF-8').split('/')

	stat_matrix = read_matrix(workdir + '/stat_matrix.pkl')
	if 'spawn' in topic:
		z = int(payload[0])
		w = int(payload[1])
		D = int(payload[2])
		x = int(payload[3])

		st = round(float(payload[4]), 3)

		stat_matrix.loc[z, 'w'] = w
		stat_matrix.loc[z, 'D'] = D
		stat_matrix.loc[z, 'x'] = x

		stat_matrix.loc[z, 'Spawn Time'] = st

	elif 'auction' in topic:
		z = int(payload[0])
		u = round(float(payload[1]), 3)

		rt = round(float(payload[2]), 3)
		at = round(float(payload[3]), 3)

		auctioned = bool(int(payload[4]))

		stat_matrix.loc[z, 'Payoff (Device)'] = u
		stat_matrix.loc[z, 'Receive Time (Spawn)'] = rt
		stat_matrix.loc[z, 'Auction Time'] = at
		stat_matrix.loc[z, 'Auctioned?'] = auctioned


	elif 'bid' in topic:
		print(topic, payload)
		z = int(payload[0])

		rt = round(float(payload[1]), 3)
		bt  = round(float(payload[2]), 3)

		stat_matrix.loc[z, 'Receive Time (Auction)'] = rt
		#if pd.isnull(stat_matrix.loc[z, 'Bid Time (First Bid)']):
		#	stat_matrix.loc[z, 'Bid Time (First Bid)'] = bt
		stat_matrix.loc[z, 'Bid Time (Last Bid)'] = bt

	elif 'offload_first' in topic:
		z = int(payload[0])
		rt = round(float(payload[1]), 3)
		stat_matrix.loc[z, 'Receive Time (First Bid)'] = rt

	elif 'offload' in topic:
		z = int(payload[0])
		y = int(payload[1])
		ug = round(float(payload[2]), 3)

		rt = round(float(payload[3]), 3)
		ot = round(float(payload[4]), 3)

		stat_matrix.loc[z, 'y'] = y
		stat_matrix.loc[z, 'Payoff (Gateway)'] = ug
		stat_matrix.loc[z, 'Offloaded?'] = bool(y)

		stat_matrix.loc[z, 'Receive Time (Last Bid)'] = rt
		stat_matrix.loc[z, 'Offload Time'] = ot

	elif 'execution' in topic:
		z = int(payload[0])

		st = round(float(payload[1]), 3)
		et = round(float(payload[2]), 3)
		pd = round(float(payload[3]), 3)

		stat_matrix.loc[z, 'Execution Time (Start)'] = st
		stat_matrix.loc[z, 'Execution Time (Finish)'] = et
		stat_matrix.loc[z, 'Projected Duration'] = pd

		stat_matrix.loc[z, 'Overdue?'] = bool((stat_matrix.loc[z, 'Receive Time (Spawn)'] + stat_matrix.loc[z, 'D']) < et)

	elif 'save' in topic:
		csv_name = payload[0]
		stat_matrix.to_csv(workdir + '/' + csv_name + '.csv')
		stat_matrix = pd.DataFrame(columns=stat_matrix.columns)

	write_matrix(stat_matrix, workdir + '/stat_matrix.pkl')

def on_connect(client, userdata, flags, rc):
	client.subscribe('edgebench/log/#')

stat_matrix = pd.DataFrame(columns = ['z', 'w', 'D', 'x', 'y', 'Payoff (Device)', 'Payoff (Gateway)', 'Spawn Time', 'Receive Time (Spawn)', 'Auction Time', 'Receive Time (Auction)', 'Bid Time (First Bid)', 'Bid Time (Last Bid)', 'Receive Time (First Bid)', 'Receive Time (Last Bid)', 'Offload Time', 'Execution Time (Start)', 'Execution Time (Finish)', 'Projected Duration', 'Overdue?', 'Auctioned?', 'Offloaded?'])
stat_matrix.set_index('z', inplace=True)
write_matrix(stat_matrix, workdir + '/stat_matrix.pkl')

client = client.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, 1883, 60)
client.loop_start()

while True:
	sleep(1)
	system('clear')
	print_logo('edgebench', -1, 'PURPLE')
	print_logo('logger')
	print('')

	stat_matrix = read_matrix(workdir + '/stat_matrix.pkl')
	print(stat_matrix)
	print('')

