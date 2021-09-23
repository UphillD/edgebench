# Edgebench Platform
# Worker Scripts
# Deployer Module
#
# Deploys a custodian and an algorithmic module in parallel
# Shows output of algorithmic module, suppresses custodian output

from os import chdir
from sys import argv
from subprocess import Popen, DEVNULL

# Print help message
if len(argv) != 4:
	print('Please provide the proper arguments!')
	print('')
	print('Usage: python3 deployer.py <module> <algorithm> <device ID>')
	print('')

else:
	# Grab information from arguments
	module = argv[1]
	algorithm = argv[2]
	device_id = argv[3]

	# Change dir to rootdir
	chdir('..')
	cmd_custodian = [ './launcher.sh', 'custode', '1,1,1,1' ]
	cmd_device = [ './launcher.sh', module, algorithm, device_id ]
	Popen(cmd_custodian, stdout=DEVNULL)
	Popen(cmd_device)
