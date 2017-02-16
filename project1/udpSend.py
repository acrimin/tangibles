import socket, pickle

def send(val):
    ip = "127.0.0.1"
    port = 5000
    print val
    data = pickle.dumps(val)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data, (ip, port))
