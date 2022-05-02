import socket

HOST = 'localhost'
PORT = 7776

s = socket.socket()

s.connect((HOST, PORT))

while True:
  data = input('')
  if not data: break
  s.send(bytearray(data, 'utf-8'))
  ans = s.recv(2048)
  print(str(ans, encoding='utf-8'))
s.close()