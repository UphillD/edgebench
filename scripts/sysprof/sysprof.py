# 4 steps
# launch a monitor
# create a monitor report
# launch an app /w perf
# generate report

from loguru import loguru
from os import chdir
from path import isfile
from sys import argv
from subprocess import Popen, DEVNULL
from time import sleep

import sysmon

app = argv[1]

apps = [[ int(argv[2]), 'deepspeech' ], 
		[ int(argv[3]), 'facenet'    ],
		[ int(argv[4]), 'lanenet'    ],
		[ int(argv[5]), 'retain'     ]]
cnt = sum(app[0] for app in apps)
logger.debug('

chdir('..')
# Launch the sysmonitor
monitor = sysmonitor()

# Launch the multilauncher
cmd = [ 'python3', 'multilauncher.py', str(apps[0][0]), str(apps[1][0]), str(apps[2][0]), str(apps[3][0]) ]
proc = Popen(cmd, stdout=DEVNULL, stderr=DEVNULL)
for i in range(cnt):
	while not isfile('/app/data/workdir/app_' + str(i+1) + '/exec.tmp'):
		sleep(0.1)


