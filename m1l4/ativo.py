import socket

HOST = 'localhost'
PORT = 3030

s = socket.socket()

s.connect((HOST, PORT))

s.send(b'Luan Martins is connecting with you!')

msg = s.recv(1024)
print(str(msg, encoding='utf-8'))

s.close()