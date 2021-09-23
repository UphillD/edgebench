# Edgebench Platform
# Helper Scripts
# Profiler Wrapper
#
# Run this from the host
# (nohup) python3 profile_wrapper.py <app> <arch> <scale> (&)

from os import chdir, system
from subprocess import Popen, PIPE, STDOUT
from sys import argv

combo_dict = {
	'1' :	[
		[1,0,0,0],
		[1,1,0,0], [1,0,1,0], [1,0,0,1],
		[1,1,1,0], [1,1,0,1], [1,0,1,1],
		[1,1,1,1]
	],
	'2' :	[
		[1,0,0,0], [2,0,0,0],
		[1,1,0,0], [1,2,0,0], [2,1,0,0], [2,2,0,0],
		[1,0,1,0], [1,0,2,0], [2,0,1,0], [2,0,2,0],
		[1,0,0,1], [1,0,0,2], [2,0,0,1], [2,0,0,2],
		[1,1,1,0], [1,1,2,0], [1,2,1,0], [1,2,2,0], [2,1,1,0], [2,1,2,0], [2,2,1,0], [2,2,2,0],
		[1,1,0,1], [1,1,0,2], [1,2,0,1], [1,2,0,2], [2,1,0,1], [2,1,0,2], [2,2,0,1], [2,2,0,2],
		[1,0,1,1], [1,0,1,2], [1,0,2,1], [1,0,2,2], [2,0,1,1], [2,0,1,2], [2,0,2,1], [2,0,2,2],
		[1,1,1,1], [1,1,1,2], [1,1,2,1], [1,1,2,2], [1,2,1,1], [1,2,1,2], [1,2,2,1], [1,2,2,2], [2,1,1,1], [2,1,1,2], [2,1,2,1], [2,1,2,2], [2,2,1,1], [2,2,1,2], [2,2,2,1], [2,2,2,2]
	]
}

# Actual execution starts here
system('clear')
system('bash print_banner.sh edgebench')
print('')
app = argv[1]
device = argv[2]
scale = argv[3]
combos = combo_dict[scale]

chdir('..')
for index, combo in enumerate(combos):
	cmd = [ './launcher.sh', 'profile', app, device, str(combo), str(index), str(len(combos)) ]
	with Popen(cmd, stdout=PIPE, stderr=STDOUT) as proc:
		for line in proc.stdout:
			line_str = line.decode('UTF-8')
			if 'combo' in line_str:
				print(line_str.replace('\n', ''))
	system("docker kill $(docker ps -a | grep 'edgebench' | cut -c1-12) >/dev/null 2>&1")
