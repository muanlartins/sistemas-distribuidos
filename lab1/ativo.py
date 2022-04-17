import socket

HOST = 'localhost'
PORT = 7776

s = socket.socket()

s.connect((HOST, PORT))

while True:
  msg = input('')
  if not msg: break
  s.send(bytearray(msg, 'utf-8'))
  ans = s.recv(2048)
  if not ans: break
  print(str(ans, encoding='utf-8'))

s.close()