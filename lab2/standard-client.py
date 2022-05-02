import socket

HOST = '10.11.0.28'
PORT = 5000

s = socket.socket()

s.connect((HOST, PORT))

# The client should receive a message, containing the list of all the files
# print(str(s.recv(2048), encoding='utf-8'))
msg = input('')

# And send a message, with the chosen option
s.send(bytearray(msg, 'utf-8'))

# Then receive the correspondent list of the frequent words
l = s.recv(2048)
print(str(l, encoding='utf-8'))

# And finally close the connection
s.close()
