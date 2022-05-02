import socket
import sys
import select

HOST = ''
PORT = 7776

entries = [sys.stdin]
connections = {}

colors = {}
colorPatternStart = '\u001b['
colorPatternEnd = 'm'
colorNumber = 32
reset = '\u001b[0m'

def startServer():
	s = socket.socket()
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	s.listen(3)
	entries.append(s)

	return s

def acceptConnection(s):
	ns, address = s.accept()
	generateColor(ns)
	print(f'Conectado com {colors[ns]}{address}{reset}.')
	ns.setblocking(False)
	entries.append(ns)
	connections[ns] = address

	return ns, address

def treatRequests(ns, address):
	data = ns.recv(1024)
	if not data: 
		print(f'Encerrado com {colors[ns]}{address}{reset}.')
		entries.remove(ns)
		del connections[ns]
		ns.close()
		return
	print(f'{colors[ns]}{str(data, encoding="utf-8")}{reset} recebido de {colors[ns]}{address}{reset}.')
	ns.send(data)

def generateColor(ns):
	global colorNumber

	colors[ns] = colorPatternStart + str(colorNumber) + colorPatternEnd
	colorNumber += 1

def printConnections():
	if not connections:
		print('Não existem conexões ativas')
	for entry in connections.keys():
		print(colors[entry] + str(connections[entry]) + reset)

def main():
	s = startServer()
	print('Servidor inicializado.')
	while True: 
		r, w, e = select.select(entries, [], [])
		for entry in r:
			if entry == s: 
				ns, address = acceptConnection(s)
			elif entry == sys.stdin:
				cmd = input('')
				if cmd == 'e': 
					if not connections:
						s.close()
						sys.exit()
					else:
						print(f'\u001b[31mAinda existem conexões ativas{reset}.')
				elif cmd == 'h':
					printConnections()
			else:
				treatRequests(entry, connections[entry])

main()