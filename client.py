import socket
import time

HOST = 'localhost'
PORT = 8001
a = '1'
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(('localhost', 8001))
time.sleep(2)
sock.send(a)
print sock.recv(1024)
sock.close()
