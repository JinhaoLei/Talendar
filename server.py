import  socket

HOST = 'localhost'
PORT = 8001

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(10)
while True:
    conn, address = sock.accept()
    print conn, address
    string = conn.recv(512)
    print string