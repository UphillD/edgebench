# Edgebench Platform
# Helper Scripts
# Multilauncher
#
# Launches multiple instances of applications
# python3 multilauncher.py a b c d (&)
#     where a b c d the number of instances for each app

from os import chdir, system
from signal import signal, SIGINT, pause
from subprocess import Popen, DEVNULL
from sys import argv
from time import sleep

def signal_handler(sig, frame):
	print('CTRL+C detected, killing edgebench...')
	system("docker kill $(docker ps -a | grep 'edgebench' | cut -c1-12) >/dev/null 2>&1")
	exit(0)
	
signal(SIGINT, signal_handler)

system('clear')
system('bash print_banner.sh edgebench')
print('')
print('Multilauncher')
apps = [[ argv[1], 'deepspeech' ], 
		[ argv[2], 'facenet' ],
		[ argv[3], 'lanenet' ],
		[ argv[4], 'retain'  ]]
cnt = 0
procs = []

chdir('..')

for app in apps:
	i = int(app[0])
	while(i > 0):
		cnt += 1
		print('Launching an instance of ' + app[1] + '.')
		cmd = [ './launcher.sh', 'loop', app[1], str(cnt) ]
		proc = Popen(cmd, stdout=DEVNULL, stderr=DEVNULL)
		procs.append(proc)
		i -= 1

while(True):
	print('Running, press CTRL+C to stop execution.')
	sleep(1)
