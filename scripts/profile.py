# edgebench/scripts/profile.py
# Call this via the profile_wrapper.py file
import csv

from glob import iglob
from numpy import mean
from subprocess import Popen, PIPE, DEVNULL, STDOUT
from os import chdir, system, path, remove
from shutil import rmtree
from sys import argv
from time import sleep

app_dict = {
	'deepspeech' : [ 'facenet', 'lanenet', 'retain' ],
	'facenet'    : [ 'deepspeech', 'lanenet', 'retain' ],
	'lanenet'    : [ 'deepspeech', 'facenet', 'retain' ],
	'retain'     : [ 'deepspeech', 'facenet', 'lanenet' ]
}

# extract time in seconds from line of output
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
	
# launch the app in question, parse output, extract execution time
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
			# print(line)
			if line.startswith(lookfor):
				secs = get_times(app, line)
				avgt.append(secs)
				c += 1
				if not c % 10:
					proc.terminate()
					return round(mean(avgt), 2)

# Actual execution starts here
platform = argv[1]
app = argv[2]
device = argv[3]
#scale = argv[4]

# chdir to /app
chdir('..')

# Print some info
system('clear')
system('bash scripts/print_banner.sh edgebench')
print('')
print('Launching profiler for {} on {}..'.format(app, device))

# Create .csv file to store results
csv_f = 'scripts/' + app + '.' + device + '.csv'
fieldnames = ['index', 'app_1', 'app_2', 'app_3', 'app_4', 'acet']
if not path.isfile(csv_f):
	with open(csv_f, mode='w') as csv_file:
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer.writeheader()
	print('CSV file created.')
else:
	print('CSV file creation skipped.')
print('')

procs = []

combo_str = argv[4]
index = int(argv[5])
length = int(argv[6])
combo = [ int(i) for i in combo_str.replace('[', '').replace(']', '').split(',') ]

#for index, combo in enumerate(combos):
# Calculate index of combo
# e.g. combo = (1,1,2,1) -> index = 1121
csv_idx = str(combo[0]*1000 + combo[1]*100 + combo[2] * 10 + combo[3])

# Check whether the combo in question has already been done
flag = False
with open(csv_f, mode='r') as csv_file:
	reader = csv.DictReader(csv_file)
	for row in reader:
		if csv_idx in row['index']:
			# flag to skip this combo
			flag = True
			acet = row['acet']
			print('Skipping  combo ({},{},{},{}) ({}/{}) : ACET = {}'.format(combo[0], combo[1], combo[2], combo[3], index + 1, length, acet))

if not flag:
	# Clean up the workdir
	path_list = iglob(path.join('./data/workdir/', 'app_*'))
	for app_path in path_list:
		if path.isdir(app_path):
			rmtree(app_path, ignore_errors=True)
	
	# Start the other apps
	cnt = 1
	for i in range(1, 4):
		for j in range(combo[i]):
			cmd = [ './entrypoint.sh', platform, 'loop', app_dict[app][i - 1], str(cnt) ]
			procs.append(Popen(cmd, stdout=DEVNULL, stderr=DEVNULL))
			cnt += 1
			
	# Start the other instances of the app in question
	for j in range(combo[0] - 1):
		cmd = [ './entrypoint.sh', platform, 'loop', app, str(cnt) ]
		procs.append(Popen(cmd, stdout=DEVNULL, stderr=DEVNULL))
		cnt += 1
	
	# Wait until all apps have begun
	for i in range(1, cnt):
		while not path.isfile('./data/workdir/app_' + str(i) + '/exec.tmp'): 
			sleep(0.1)
	
	acet = get_acet(app, cnt)
	print('Completed combo ({},{},{},{}) ({}/{}) : ACET = {}'.format(combo[0], combo[1], combo[2], combo[3], index + 1, length, acet))
	
	#system("docker kill $(docker ps -a | grep 'edgebench' | cut -c1-12) >/dev/null 2>&1") 
	#system("docker container prune -f >/dev/null 2>&1")
	
	# Send SIGTERM TO all instances
	for proc in procs:
		proc.terminate()
	
	# Store the result
	with open(csv_f, mode='a') as csv_file:
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer.writerow({
			'index' : str(csv_idx), 
			'app_1' : str(combo[0]), 
			'app_2' : str(combo[1]), 
			'app_3' : str(combo[2]), 
			'app_4' : str(combo[3]), 
			'acet'  : str(acet)
		})
