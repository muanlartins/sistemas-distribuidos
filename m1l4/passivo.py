import socket

HOST = ''
PORT = 3030

s = socket.socket()

s.bind((HOST, PORT))

s.listen(1)

ns, address = s.accept()

print('Connected with: ' + str(address))

while True:
  msg = ns.recv(1024)
  if not msg: break
  print(str(msg, encoding='utf-8'))
  ns.send(b'Congratulations on connecting with Luan Martins!')

ns.close()
s.close()