import socket, pickle

def recv():
	ip = "127.0.0.1"
	port = 5000
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((ip, port))
	
	val = sock.recvfrom(4096)
	data = pickle.loads(val[0])
	
	print data
	
recv()