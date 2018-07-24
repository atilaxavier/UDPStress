# udp_stress_client_t.py by Atila Xavier
# Modifications/additions:
# 1 - Definition of server IP address and port on the command line (optional)
# 2 - Random characters string to be sent on each iteration
# 3 - Added option to insert wait time (sleep) between bursts

# Based on udp_stress_client.py by Eli Fulkerson on 20/07/2018
# http://www.elifulkerson.com for base version
# You will also need udp_stress_server.py for this to do anything for you.

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


#from socket import *
import socket
import string
import time
import argparse
import random

# Using arguments to get server (destination) IP address and port (optionals)
parser = argparse.ArgumentParser(description='udp_stress_client_t.py. UDP packets generator client.')
parser.add_argument('-a', '--server_addres', dest='host', default='localhost',
					help='Destination server IP address (optional)')
parser.add_argument('-p', '--server_port', dest='port', type=int, default=8105,
					help='Destination server Port number (optional)')
parser.add_argument('-w', '--wait', dest='wait_time', type=float, default=1e-09,
					help='Wait time between bursts, in seconds, if greater then 1e-06 (optional)')
inarg = parser.parse_args()
host = inarg.host
port = inarg.port
wait_time = inarg.wait_time

UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("\nStarting client end.  Control-C to quit.")

print("\nOur target:")
print("udp_stress_server.py running on %s port %s" % (host, port))
if wait_time > 1e-06:
	print("Pause between bursts of %f seconds" %wait_time)
	

print("\n\nEnter number of bytes to send and the number of times to send them:\n(for instance '100 10' to send 10 bursts of 100 bytes each)");

while True:
	data = input('% ')
	args = data.split()
	print(args)

	try:
		if args[0] == "reset":
			data = "X"
			numtimes = 1
		else:      
			numtimes = int(args[1])
			data = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(int (args[0])))
			#data = "X" * int(args[0])
			#numtimes = int(args[1])
	except:
			data = None
			numtimes = None
			print("Error, you need to specify two numbers.  First the number of bytes to send, second the number of times to send them.")
                
	if not data:
		pass
	else:
		try:
			#the resetter...
			# sending number of bursts and size of each burst in the format: #<numbytes>#<numtimes>
			reset_str = '#'+str(len(data))+'#'+str(numtimes)
			UDPSock.sendto(bytes(reset_str, 'utf-8'), (host,port))
			
			for x in range(numtimes):
				if(UDPSock.sendto(bytes(data, 'utf-8'),(host,port))):
					print("*", end=' ')
					if wait_time > 1e-06:
						print("Pause %f seconds\n" %wait_time)
						time.sleep(wait_time)
				else:
					print(".")
						
					# a pause via time.sleep()
					# not sure that this is needed.  Put it here to play with maybe not-overloading the
					# windows tcp/ip stack, but not sure if it actually has any noticable effect.
					print("Socket send error. Pause before sending again....\n")
					time.sleep(0.0001)

					
			print("Done.")

		except:
			print("Send failed")


UDPSock.close()
