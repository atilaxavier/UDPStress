# udp_stress_server.py by Atila Xavier
# modifications/additions:
# 1 - Definition of buffer size and port on the command line (optional)
# 2 - Identification and printing of server IP address

# Based on udp_stress_server.py by Eli Fulkerson on 20/07/2018
# http://www.elifulkerson.com for base version
# You will also need udp_stress_client.py for this to do anything for you.

# "Push it to the limit!"

# This is an extremely quick-and-dirty UDP testing utility.
# All it does is shove a bunch of UDP traffic through to the server, which
# records and reports the amount of data successfully recieved and the time
# that the transmission took.  It spits out the ratio to give a rough kbps
# estimate.

# The results are very dependent on how much data you push through.  Low amounts
# of data will give you artificially low results.

# "Safety is not guaranteed."

# July 20 2018

import socket
import time
import argparse

# we want to bind on all possible IP addresses
host = "0.0.0.0"

#if you change the port, change it in the client program as well
port = 8105
buffer = 102400

# Using arguments to get port to be listened and buffer size (optionals)
parser = argparse.ArgumentParser(description='udp_stress_server.py. UDP packets receiver server.')
parser.add_argument('-b', '--buffer_size', dest='buffer', type=int, default=102400,
					help='Server Buffer size (optional)')
parser.add_argument('-p', '--server_port', dest='port', type=int, default=8105,
					help='Server Port number (optional)')
inarg = parser.parse_args()
buffer = inarg.buffer
port = inarg.port

print("\n")
print("-" * 40)
print("udp_stress_server.py")
print("-" * 40)
print("\n")
print('Listening on port: %d with buffer size: %d' %(port, buffer))
# Create socket and bind to address
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock.bind((host,port))
try:
	UDPSock.connect(('8.8.8.8', 1))
	myIP = UDPSock.getsockname()[0]
except:
	myIP = '127.0.0.1'
finally:
	UDPSock.close()
print("\n")
print("my IP: %s" % myIP)

UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock.bind((host,port))

time.time()

print("Starting UDP receive server...  control-break to exit.\n")
print("\nWaiting for data...")

# total bytes recieved since last 'reset'
totalbytes = 0

# expectes bytes per bursts
ex_bytesperburst = 0

# -1 is a deliberately invalid timestamp
timestamp = -1

# the total number of bursts that have come in
totalrcvs = 0

# expected bursts to be received
ex_numbursts = 0

# expected total bytes to be received
ex_totalbytes = 0

while True:
	data,addr = UDPSock.recvfrom(buffer)
	
	if not data:
		print("No data.")
		break
	else:
		donestamp = time.time()
		data_len = len(data)
		#data_str = str(data)
		#print(data_str)
		#print(data[0])

		if data[0] == ord('#'):
			# this is the reset, in the format: in the format: #<numbytes>#<numbursts>
			totalbytes = 0
			timestamp = time.time()
			totalrcvs = 0
			print("Reset received, clearing statistics.")
			data_str = str(data, 'utf-8')
			ex_bytesperburst = int(data_str.split('#')[1])
			ex_numbursts = int(data_str.split('#')[2])
			ex_totalbytes = ex_bytesperburst * ex_numbursts
			print("Expect %d bursts with %d bytes - total: %d bytes" %(ex_numbursts, ex_bytesperburst, ex_totalbytes))
		else:
			totalbytes += data_len
			totalrcvs += 1
			tdif = donestamp-timestamp
			if tdif == 0.0:
				tdif = 0.0000001
			rate = (8 / 1000) * totalbytes/(tdif)
			print("\nRcvd: %s bytes, %s total in %s s at %s kbps" % (data_len, totalbytes, tdif, rate))
			if data_len < ex_bytesperburst:
				print("\nLOST %d BYTES\n" % (ex_bytesperburst-data_len))
			print('Missing %d bytes - %3.4f %% packet loss' %(ex_totalbytes - totalbytes, 1-(totalbytes/ex_totalbytes)))

UDPSock.close()
