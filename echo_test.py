# echo_test.py by Atila Xavier
# TCP or UDP echo test client.
# July 23 2018

import socket
import time
import argparse
import threading

# we want to bind on all possible IP addresses
BUFF = 1024


# Using arguments to get port to be listened and buffer size (optionals)
parser = argparse.ArgumentParser(description="echo_test.py. TCP or UDP echo client."\
									" Sends message and shows the echoed message." \
									"Example (TCP): python echo_test.py -a echo.u-blox.com -p 7 -t True" \
									"Example (UDP): python echo_test.py -a echo.u-blox.com -p 7")
parser.add_argument('-t', '--tcp', dest='tcp', type=bool, default=False,
					help='TCP connection - default False (optional)')
parser.add_argument('-a', '--server_address', dest='addr', type=str, default="127.0.0.1",
					help='Server Address')
parser.add_argument('-p', '--server_port', dest='port', type=int, default=7,
					help='Server Port number (optional)')
inarg = parser.parse_args()
tcp = inarg.tcp
addr = inarg.addr
port = inarg.port

print("\n")
print("-" * 40)
print("echo_test.py")
print("-" * 40)
print("\n")
if (tcp):
	print('Sending to server %s on port: %d with TCP' %(addr, port))
else:
	print('Sending to server %s on port: %d with UDP' %(addr, port))
	
if (tcp):
	sock = socket.socket(socket.AF_INET, 
					socket.SOCK_STREAM) #TCP
else:
	sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP	
sock.connect((addr, port))

if (tcp):
	data = sock.recv(BUFF)
	print ("Connected to: %s\n" % str(data, 'utf-8'))

while True:
	msg = input("Mensagem (bye to exit): ")
	if msg in ('bye', 'exit', 'tchau'):
		print("finalizando")
		if (tcp):
			sock.close()
		break;
	else:
		print ("Sending message: %s \n" % (msg))
		sock.send(bytes(msg, 'utf-8'))
		if (tcp):
			data = sock.recv(BUFF)
			print ("Received from TCP message: %s\n" % str(data, 'utf-8'))
		else:
			data, addr_rec = sock.recvfrom(BUFF)
			print ("Received from %s - message: %s\n" % (addr_rec, str(data, 'utf-8')))

