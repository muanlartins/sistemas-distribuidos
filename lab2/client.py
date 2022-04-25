import socket

HOST = 'localhost'
PORT = 7776

s = socket.socket()

s.connect((HOST, PORT))

msg = input('')
s.send(bytearray(msg, 'utf-8'))
l = s.recv(2048)
print(str(l, encoding='utf-8'))

s.close()