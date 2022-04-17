import socket

HOST = ''
PORT = 7776

s = socket.socket()

s.bind((HOST, PORT))
s.listen(1)
ns, address = s.accept()

while True:
  msg = ns.recv(2048)
  if not msg: break

  print(str(msg, encoding='utf-8'))

  ns.send(msg)

ns.close()
s.close()