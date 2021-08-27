from os import chdir, system
from sys import argv
from subprocess import Popen, DEVNULL
from time import sleep

module = argv[1]
algorithm = argv[2]
device_id = argv[3]

chdir('..')
cmd_custodian = [ './launcher.sh', 'custode', '2,2,2,2' ]
cmd_device = [ './launcher.sh', module, algorithm, device_id ]
Popen(cmd_custodian, stdout=DEVNULL)
Popen(cmd_device)



"""
gen = print_progress_bar()
while True:
	try:
		system('clear')
		print_logo(algorithm.lower())
		print_logo(module, int(device_id), 'PURPLE')
		print('')
		print('Press CTRL+C to stop execution...')
		print('')
		next(gen)
		sleep(0.3)
	except KeyboardInterrupt:
		system('docker kill $(docker ps -q)')
		print('Execution concluded')
		exit(0)

"""
