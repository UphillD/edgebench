import csv

from glob import iglob
from numpy import mean
from subprocess import Popen, PIPE, DEVNULL, STDOUT
from os import chdir, system, path, remove
from shutil import rmtree
from sys import argv
from time import sleep

"""
combos = [
	[1,0,0,0],
	[1,1,0,0], [1,0,1,0], [1,0,0,1],
	[1,1,1,0], [1,1,0,1], [1,0,1,1],
	[1,1,1,1]
]
"""

combos =   [
	[1,0,0,0], [2,0,0,0],
	[1,1,0,0], [1,2,0,0], [2,1,0,0], [2,2,0,0],
	[1,0,1,0], [1,0,2,0], [2,0,1,0], [2,0,2,0],
	[1,0,0,1], [1,0,0,2], [2,0,0,1], [2,0,0,2],
	[1,1,1,0], [1,1,2,0], [1,2,1,0], [1,2,2,0], [2,1,1,0], [2,1,2,0], [2,2,1,0], [2,2,2,0],
	[1,1,0,1], [1,1,0,2], [1,2,0,1], [1,2,0,2], [2,1,0,1], [2,1,0,2], [2,2,0,1], [2,2,0,2],
	[1,0,1,1], [1,0,1,2], [1,0,2,1], [1,0,2,2], [2,0,1,1], [2,0,1,2], [2,0,2,1], [2,0,2,2],
	[1,1,1,1], [1,1,1,2], [1,1,2,1], [1,1,2,2], [1,2,1,1], [1,2,1,2], [1,2,2,1], [1,2,2,2], [2,1,1,1], [2,1,1,2], [2,1,2,1], [2,1,2,2], [2,2,1,1], [2,2,1,2], [2,2,2,1], [2,2,2,2]
]

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
	cmd = [ './entrypoint.sh', platform, 'loop', app, str(cnt) ]
	with Popen(cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, universal_newlines=True) as proc:
		for line in proc.stdout:
			if line.startswith(lookfor):
				secs = get_times(app, line)
				avgt.append(secs)
				c += 1
				if not c % 10:
					proc.terminate()
					return round(mean(avgt), 2)


platform = argv[1]
app = argv[2]
device = argv[3]

system('clear')
print('Launching edgebench profiler for {}'.format(app))

with open(app + '.' + device + '.csv', mode='w') as csv_file:
	fieldnames = ['index', 'app_1', 'app_2', 'app_3', 'app_4', 'acet']
	writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
	writer.writeheader()

print('CSV file created.')
	

chdir('..')
procs = []

for index, combo in enumerate(combos):
	print('Running combo ({},{},{},{}) ({}/{})'.format(combo[0], combo[1], combo[2], combo[3], index + 1, len(combos)))
	
	path_list = iglob(path.join('./data/workdir/', 'app_*'))
	for app_path in path_list:
		if path.isdir(app_path):
			rmtree(app_path, ignore_errors=True)
	
	cnt = 1
	for i in range(1, 4):
		for j in range(combo[i]):
			cmd = [ './entrypoint.sh', platform, 'loop', app_dict[app][i - 1], str(cnt) ]
			procs.append(Popen(cmd, stdout=DEVNULL, stderr=DEVNULL))
			cnt += 1
	
	for j in range(combo[0] - 1):
		cmd = [ './entrypoint.sh', platform, 'loop', app, str(cnt) ]
		procs.append(Popen(cmd, stdout=DEVNULL, stderr=DEVNULL))
		cnt += 1
	
	# Wait until all apps have begun
	for i in range(1, cnt):
		while not path.isfile('./data/workdir/app_' + str(i) + '/exec.tmp'): 
			sleep(0.1)
	
	acet = get_acet(app, cnt)
	#print('ACET = {}'.format(str(acet)))
	#print('')
	
	#system("docker kill $(docker ps -a | grep 'edgebench' | cut -c1-12) >/dev/null 2>&1") 
	#system("docker container prune -f >/dev/null 2>&1")
	
	for proc in procs:
		proc.terminate()
	
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
