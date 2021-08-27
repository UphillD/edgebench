# Shared
# Collection of shared functions and settings
import pandas as pd
import pickle as pkl

from os import path, remove
from pathlib import Path

from config import *

# List of applications
apps = [ 'deepspeech', 'facenet', 'lanenet', 'retain' ]

# read/write matrix functions
def read_matrix(input_file):
	return_matrix = pd.read_pickle(input_file)
	#with open(input_file, 'rb') as f:
	#	return_matrix = pkl.load(f)
	return return_matrix

def write_matrix(input_matrix, output_file):
	input_matrix.to_pickle(output_file)
	#with open(output_file, 'wb') as f:
		#pkl.dump(input_matrix, f)
	return

def remove_matrix(input_file):
	if path.exists(input_file):
		remove(input_file)
	return

def categorize_task(w):
	if w == 0:
		return 'deepspeech', 'payload.wav'
	elif w == 1:
		return 'facenet', 'payload.jpg'
	elif w == 2:
		return 'lanenet', 'payload.jpg'
	elif w == 3:
		return 'retain', 'payload.zip'

def calculate_size(w):
	if w == 0:
		return 262700
	elif w == 1:
		return 2560
	elif w == 2:
		return 187658
	elif w == 3:
		return 3830


# https://stackoverflow.com/questions/35277075/python-pandas-counting-the-occurrences-of-a-specific-value
def sum_mask_numpy(df, w):
    return (df.w.values == w).sum()

# 
# AESTHETICS
# 
color_dict = {
	'BLACK'     : '\033[1;30;48m',
	'RED'       : '\033[1;31;48m',
	'GREEN'     : '\033[1;32;48m',
	'YELLOW'    : '\033[1;33;48m',
	'BLUE'      : '\033[1;34;48m',
	'PURPLE'    : '\033[1;35;48m',
	'CYAN'      : '\033[1;36;48m',
	'BOLD'      : '\033[1;37;48m',
	'UNDERLINE' : '\033[4;37;48m',
	'END'       : '\033[1;37;0m'
}

logo_dict = {
	'sgrm': [
		" .M\"\"\"bgd   .g8\"\"\"bgd `7MM\"\"\"Mq.  `7MMM.     ,MMF'",
		",MI    \"Y .dP'     `M   MM   `MM.   MMMb    dPMM  ",
		"`MMb.     dM'       `   MM   ,M9    M YM   ,M MM  ",
		"  `YMMNq. MM            MMmmdM9     M  Mb  M' MM  ",
		".     `MM MM.    `7MMF' MM  YM.     M  YM.P'  MM  ",
		"Mb     dM `Mb.     MM   MM   `Mb.   M  `YM'   MM  ",
		"P\"Ybmmd\"    `\"bmmmdPY .JMML. .JMM..JML. `'  .JMML." ],
	'oracle': [
		" ▒█████   ██▀███   ▄▄▄       ▄████▄   ██▓    ▓█████ ",
		"▒██▒  ██▒▓██ ▒ ██▒▒████▄    ▒██▀ ▀█  ▓██▒    ▓█   ▀ ",
		"▒██░  ██▒▓██ ░▄█ ▒▒██  ▀█▄  ▒▓█    ▄ ▒██░    ▒███   ",
		"▒██   ██░▒██▀▀█▄  ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▒██░    ▒▓█  ▄ ",
		"░ ████▓▒░░██▓ ▒██▒ ▓█   ▓██▒▒ ▓███▀ ░░██████▒░▒████▒",
		"░ ▒░▒░▒░ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ░▒ ▒  ░░ ▒░▓  ░░░ ▒░ ░",
		"  ░ ▒ ▒░   ░▒ ░ ▒░  ▒   ▒▒ ░  ░  ▒   ░ ░ ▒  ░ ░ ░  ░" ],
	'nooffload': [
		"   ▄   ████▄     ████▄ ▄████  ▄████  █    ████▄ ██   ██▄   ",
		"    █  █   █     █   █ █▀   ▀ █▀   ▀ █    █   █ █ █  █  █  ",
		"██   █ █   █ ███ █   █ █▀▀    █▀▀    █    █   █ █▄▄█ █   █ ",
		"█ █  █ ▀████     ▀████ █      █      ███▄ ▀████ █  █ █  █  ",
		"█  █ █                  █      █         ▀         █ ███▀  ",
		"█   ██                   ▀      ▀                 █        ",
		"                                                 ▀         " ],
	'device': [
		"	                   ┌┬┐┌─┐┬  ┬┬┌─┐┌─┐",
		"	                    ││├┤ └┐┌┘││  ├┤ ",
		"	                   ─┴┘└─┘ └┘ ┴└─┘└─┘" ],
	'gateway': [
		"	               ┌─┐┌─┐┌┬┐┌─┐┬ ┬┌─┐┬ ┬",
		"	               │ ┬├─┤ │ ├┤ │││├─┤└┬┘",
		"	               └─┘┴ ┴ ┴ └─┘└┴┘┴ ┴ ┴ " ],
	'custodian': [
		"	         ┌┬┐┬ ┬┌─┐  ┌─┐┬ ┬┌─┐┌┬┐┌─┐┌┬┐┬┌─┐┌┐┌",
		"	          │ ├─┤├┤   │  │ │└─┐ │ │ │ │││├─┤│││",
		"	          ┴ ┴ ┴└─┘  └─┘└─┘└─┘ ┴ └─┘─┴┘┴┴ ┴┘└┘" ],
	'logger': [
		"	                ┌┬┐┬ ┬┌─┐  ┬  ┌─┐┌─┐┌─┐┌─┐┬─┐",
		"	                 │ ├─┤├┤   │  │ ││ ┬│ ┬├┤ ├┬┘",
		"	                 ┴ ┴ ┴└─┘  ┴─┘└─┘└─┘└─┘└─┘┴└─" ],
	'spawner': [
		"	             ┌┬┐┬ ┬┌─┐  ┌─┐┌─┐┌─┐┬ ┬┌┐┌┌─┐┬─┐",
		"	              │ ├─┤├┤   └─┐├─┘├─┤││││││├┤ ├┬┘",
		"	              ┴ ┴ ┴└─┘  └─┘┴  ┴ ┴└┴┘┘└┘└─┘┴└─" ],
	'0': [
		"┌─┐",
		"│ │",
		"└─┘" ],
	'1': [
		" ┐ ",
		" │ ",
		" ┴ " ],
	'2': [
		"┌─┐",
		"┌─┘",
		"└─┘" ],
	'3': [
		"┌─┐",
		" ─┤",
		"└─┘" ],
	'4': [
		"┬ ┬",
		"└─┤",
		"  ┴" ],
	'5': [
		"┌─┐",
		"└─┐",
		"└─┘" ],
	'6': [
		"┌─┐",
		"├─┐",
		"└─┘" ],
	'7': [
		"┌─┐",
		"  │",
		"  ┴" ],
	'8': [
		"┌─┐",
		"├─┤",
		"└─┘" ],
	'9': [
		"┌─┐",
		"└─┤",
		"└─┘" ]
}
	
def print_progress_bar():
	while True:
		print(color_dict['CYAN'] + '                                                ██    ' + color_dict['END'])
		print(color_dict['CYAN'] + '                                                      ' + color_dict['END'])
		print(color_dict['CYAN'] + '                                                      ' + color_dict['END'])
		yield
		print(color_dict['PURPLE'] + '                                                ████  ' + color_dict['END'])
		print(color_dict['PURPLE'] + '                                                ██    ' + color_dict['END'])
		print(color_dict['PURPLE'] + '                                                      ' + color_dict['END'])
		yield
		print(color_dict['CYAN'] + '                                                ██████' + color_dict['END'])
		print(color_dict['CYAN'] + '                                                ████  ' + color_dict['END'])
		print(color_dict['CYAN'] + '                                                ██    ' + color_dict['END'])
		yield
		print(color_dict['PURPLE'] + '                                                ██████' + color_dict['END'])
		print(color_dict['PURPLE'] + '                                                ██████' + color_dict['END'])
		print(color_dict['PURPLE'] + '                                                ████  ' + color_dict['END'])
		yield
		print(color_dict['CYAN'] + '                                                ██████' + color_dict['END'])
		print(color_dict['CYAN'] + '                                                ██████' + color_dict['END'])
		print(color_dict['CYAN'] + '                                                ██████' + color_dict['END'])
		yield
		print(color_dict['PURPLE'] + '                                                  ████' + color_dict['END'])
		print(color_dict['PURPLE'] + '                                                ██████' + color_dict['END'])
		print(color_dict['PURPLE'] + '                                                ██████' + color_dict['END'])
		yield
		print(color_dict['CYAN'] + '                                                    ██' + color_dict['END'])
		print(color_dict['CYAN'] + '                                                  ████' + color_dict['END'])
		print(color_dict['CYAN'] + '                                                ██████' + color_dict['END'])
		yield
		print(color_dict['PURPLE'] + '                                                      ' + color_dict['END'])
		print(color_dict['PURPLE'] + '                                                    ██' + color_dict['END'])
		print(color_dict['PURPLE'] + '                                                  ████' + color_dict['END'])
		yield
		print(color_dict['CYAN'] + '                                                      ' + color_dict['END'])
		print(color_dict['CYAN'] + '                                                      ' + color_dict['END'])
		print(color_dict['CYAN'] + '                                                    ██' + color_dict['END'])
		yield
		print(color_dict['PURPLE'] + '                                                      ' + color_dict['END'])
		print(color_dict['PURPLE'] + '                                                      ' + color_dict['END'])
		print(color_dict['PURPLE'] + '                                                      ' + color_dict['END'])
		yield
		

def print_logo(name, number=-1, color='CYAN'):
	if number >= 0:
		for i in range(len(logo_dict[name])):
			print(color_dict[color] + logo_dict[name][i] + "   " + logo_dict[str(number)][i] + color_dict['END'])
	else:
		for i in range(len(logo_dict[name])):
			print(color_dict[color] + logo_dict[name][i] + color_dict['END'])
	
