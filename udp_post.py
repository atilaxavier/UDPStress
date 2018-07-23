import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
#MESSAGE = "Ola servidor. Essa é uma mensagem via UDP."
print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)

while True:
	msg = input("Mensagem: ")
	if msg in ('bye', 'tchau'):
		print("finalizando")
		break;
	else:
		print ("message:", msg)
		sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
		sock.sendto(bytes(msg, 'utf-8'), (UDP_IP, UDP_PORT))
