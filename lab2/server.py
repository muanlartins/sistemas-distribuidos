import socket

HOST = ''
PORT = 7776

s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))
s.listen(1)

print('Servidor inicializado')

while True:
  ns, address = s.accept()

  print(f'Servidor conectado com {address}', )

  msg = ns.recv(2048)
  print(str(msg, encoding='utf-8'))

  try:
    with open(msg, 'r') as f:

      frequencies = {}

      # Add every word from the file into a dictionary to count frequencies
      for line in f:
        for word in line.split():
          lowerWord = word.lower()
          if frequencies.__contains__(lowerWord): frequencies[lowerWord] += 1 
          else: frequencies[lowerWord] = 1
      
      # Sort frequencies dictionary based on value, decreasing order
      frequencies = dict(sorted(frequencies.items(), key=lambda p: p[1], reverse=True))

      # Prepare the message containing 5 words, from most frequent to least frequent
      l = ''
      i = 0
      for word in frequencies.keys():
        l += word
        i += 1
        if i == 5: break
        l += '\n'

      ns.send(bytearray(l, encoding='utf-8'))
  
  except IOError: 
    # In case of an error with the file
    ns.send(b'Nome de arquivo inexistente')

  ns.close()
s.close()