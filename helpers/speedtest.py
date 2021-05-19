from paho.mqtt import publish, subscribe
from sys import argv
from time import time, sleep

def find_payload(w):
	if w == '0':
		return '../data/payloads/deepspeech/payload.wav'
	elif w == '1':
		return '../data/payloads/facenet/payload.jpg'
	elif w == '2':
		return '../data/payloads/lanenet/payload.jpg'
	elif w == '3':
		return '../data/payloads/retain/payload.zip'

broker = '147.102.37.73'

if argv[1] == 'pub':
	payload_path = find_payload(argv[2])
	payload_file = open(payload_path, 'rb')
	imageString = payload_file.read()
	byteArray = bytes(imageString)
	t = time()
	publish.single('speedtest/1', byteArray, qos=0, hostname=broker)
	print("Test file sent!")
	subscribe.simple('speedtest/2', qos=1, hostname=broker)
	print("Confirmation file received!")
	
	t = time() - t
	speed = (262700 / t) / 1000 / 1000
	print('Time: {:.2f} sec'.format(t))
	print('Speed: {:.2f} MBps'.format(speed))
	
	#publish.single('speedtest/3', t, qos=1, hostname=broker)
	
elif argv[1] == 'sub':
	subscribe.simple('speedtest/1', qos=1, hostname=broker)
	print("Test file received!")
	sleep(1)
	publish.single('speedtest/2', '', qos=1, hostname=broker)
	print("Confirmation file sent!")
