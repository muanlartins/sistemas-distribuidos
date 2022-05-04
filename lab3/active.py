import socket

HOST = 'localhost'
PORT = 7776

s = socket.socket()

s.connect((HOST, PORT))

while True:
  # The client should receive a message, containing the list of all the files
  # print(str(s.recv(2048), encoding='utf-8'))
  msg = input('')

  if not msg:
    s.close()
    break

  # And send a message, with the chosen option
  s.send(bytearray(msg, 'utf-8'))

  # Then receive the correspondent list of the frequent words
  l = s.recv(2048)
  print(str(l, encoding='utf-8'))


# And finally close the connection
s.close()