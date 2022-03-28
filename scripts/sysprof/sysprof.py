# 4 steps
# launch a monitor
# create a monitor report
# launch an app /w perf
# generate report

from os import chdir
from sys import argv
from subprocess import Popen, DEVNULL
from time import sleep

import sysmon

app = argv[1]

apps = [[ argv[2], 'deepspeech' ], 
		[ argv[3], 'facenet' ],
		[ argv[4], 'lanenet' ],
		[ argv[5], 'retain'  ]]

chdir('..')
# Launch the sysmonitor
monitor = sysmonitor()

# Launch the multilauncher
cmd = [ 'python3', 'multilauncher.py', 'argv[2]', 'argv[3]', 'argv[4]', 'argv[5]' ]
proc = Popen(cmd, stdout=DEVNULL, stderr=DEVNULL)

# Wait for some time
sleep(30)

# Run the app
