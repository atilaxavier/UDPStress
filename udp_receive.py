import socket, sys

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
n_rec_msg = 0

sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


try:
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		print ("received message: ", str(data, 'utf-8'))
		n_rec_msg += 1
except KeyboardInterrupt:
	print("CTRL-C detectado. Derrubando servidor. Msgs recebidas:", n_rec_msg)
	sys.stdout.flush()
	sys.exit()
finally:
	print("finally CTRL-C detectado. Derrubando servidor. Msgs recebidas:", n_rec_msg)


