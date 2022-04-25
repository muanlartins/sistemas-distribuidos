import socket, glob

HOST = ''
PORT = 7776

s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))
s.listen(1)

print('Servidor inicializado')

while True:
  print('Aguardando nova conexão...')

  ns, address = s.accept()

  print(f'Servidor conectado com {address}', )

  # Send message listing all options
  files = {}
  fileCount = 0
  for file in glob.glob("./*.txt"):
    files[fileCount] = file
    fileCount += 1
  
  options = 'Escolha sua opção (número):'
  for key in files:
    options += f'\n{str(key)}: {files[key]}'

  ns.send(bytearray(options, encoding='utf-8'))


  msg = ns.recv(2048)
  msg = str(msg, encoding='utf-8')
  print(f'Opção escolhida: {msg}.')

  # In case of an error with the file
  try:
    if msg.isnumeric() == False:
      raise Exception()
    elif files.__contains__(int(msg)) == False:
      raise Exception()
  except:
    print('Opção inválida')
    ns.send(bytearray('Opção inválida', encoding='utf-8')) 
    ns.close()
    continue


  f = open(files[int(msg)], 'r')

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

  ns.close()
s.close()