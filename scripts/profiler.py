import csv

from numpy import mean
from subprocess import Popen, PIPE, DEVNULL
from os import chdir, system, path, remove
from sys import argv
from time import sleep
import shutil
import glob


combos = [
	[1,0,0,0],
	[1,1,0,0], [1,0,1,0], [1,0,0,1],
	[1,1,1,0], [1,1,0,1], [1,0,1,1],
	[1,1,1,1]
]

"""
combos =   [
	#[1,0,0,0], [2,0,0,0],
	[2,0,0,0],
	[1,1,0,0], [1,2,0,0], [2,1,0,0], [2,2,0,0],
	[1,0,1,0], [1,0,2,0], [2,0,1,0], [2,0,2,0],
	[1,0,0,1], [1,0,0,2], [2,0,0,1], [2,0,0,2],
	[1,1,1,0], [1,1,2,0], [1,2,1,0], [1,2,2,0], [2,1,1,0], [2,1,2,0], [2,2,1,0], [2,2,2,0],
	[1,1,0,1], [1,1,0,2], [1,2,0,1], [1,2,0,2], [2,1,0,1], [2,1,0,2], [2,2,0,1], [2,2,0,2],
	[1,0,1,1], [1,0,1,2], [1,0,2,1], [1,0,2,2], [2,0,1,1], [2,0,1,2], [2,0,2,1], [2,0,2,2],
	[1,1,1,1], [1,1,1,2], [1,1,2,1], [1,1,2,2], [1,2,1,1], [1,2,1,2], [1,2,2,1], [1,2,2,2], [2,1,1,1], [2,1,1,2], [2,1,2,1], [2,1,2,2], [2,2,1,1], [2,2,1,2], [2,2,2,1], [2,2,2,2]
]
"""

app_dict = {
	'deepspeech' : [ 'facenet', 'lanenet', 'retain' ],
	'facenet'    : [ 'deepspeech', 'lanenet', 'retain' ],
	'lanenet'    : [ 'deepspeech', 'facenet', 'retain' ],
	'retain'     : [ 'deepspeech', 'facenet', 'lanenet' ]
}

def get_times(app, line):
	if app == 'deepspeech':
		res = line[4:].lstrip().rstrip()
		mins = res[:res.find('m')]
		secs = res[res.find('m')+1:res.find('s')]
		secs = (int(mins) * 60) + float(secs)
	elif app == 'facenet':
		res = line[18:].lstrip().rstrip()
		secs = float(res[:res.find('s')])
	elif app == 'lanenet':
		res = line[5:].lstrip()
		secs = float(res[:res.find('s')])
	elif app == 'retain':
		res = line[4:].lstrip().rstrip()
		mins = res[:res.find('m')]
		secs = res[res.find('m')+1:res.find('s')]
		secs = (int(mins) * 60) + float(secs)
	
	return secs
	
def get_acet(app, cnt):
	avgt = []
	if app == 'deepspeech':
		lookfor = 'real'
	elif app == 'facenet':
		lookfor = 'Image inferred in'
	elif app == 'lanenet':
		lookfor = 'ACET'
	elif app == 'retain':
		lookfor = 'real'
	
	c = 0
		
	cmd = [ './launcher.sh', 'loop', app, str(cnt) ]
	with Popen(cmd, stdout=PIPE, bufsize=1, universal_newlines=True) as proc:
		for line in proc.stdout:
			if line.startswith(lookfor):
				break
		for line in proc.stdout:
			if line.startswith(lookfor):
				secs = get_times(app, line)
				avgt.append(secs)
				c += 1
				if not c % 10:
					return mean(avgt)

app = argv[1]
device = argv[2]

with open(app + '.' + device + '.csv', mode='w') as csv_file:
	fieldnames = ['index', 'app_1', 'app_2', 'app_3', 'app_4', 'acet']
	writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
	writer.writeheader()

print('CSV file created.')
	

chdir('..')

for combo in combos:
	print('Running combo ({},{},{},{}).'.format(str(combo[0]), str(combo[1]), str(combo[2]), str(combo[3])))
	
	
	path_list = glob.iglob(path.join('./algo/workdir/', 'app_*'))
	for apppath in path_list:
		if path.isdir(apppath):
			shutil.rmtree(apppath)
	
	cnt = 1
	for i in range(1, 4):
		for j in range(combo[i]):
			cmd = [ './launcher.sh', 'loop', app_dict[app][i - 1], str(cnt) ]
			Popen(cmd, stdout=DEVNULL)
			cnt += 1
	
	for j in range(combo[0] - 1):
		cmd = [ './launcher.sh', 'loop', app, str(cnt) ]
		Popen(cmd, stdout=DEVNULL)
		cnt += 1
	
	# Wait until all apps have begun
	for i in range(1, cnt):
		while not path.isfile('./algo/workdir/app_' + str(i) + '/exec.tmp'): 
			sleep(0.1)
		else:
			print('Background apps ready!')
	
	acet = get_acet(app, cnt)
	print('ACET = {}'.format(str(acet)))
	
	system("docker kill $(docker ps -a | grep 'edgebench' | cut -c1-12)")
	system('docker container prune -f')
	
	with open('./scripts/' + app + '.' + device + '.csv', mode='a') as csv_file:
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer.writerow({
			'index' : str(combo[0]*1000 + combo[1]*100 + combo[2] * 10 + combo[3]), 
			'app_1' : str(combo[0]), 
			'app_2' : str(combo[1]), 
			'app_3' : str(combo[2]), 
			'app_4' : str(combo[3]), 
			'acet'  : str(acet)
		})
