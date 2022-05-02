import socket
import sys
import select
import threading

HOST = ''
PORT = 7776

entries = [sys.stdin]
connections = {}
lock = threading.Lock()

colors = {}
colorPatternStart = '\u001b['
colorPatternEnd = 'm'
colorNumber = 32
reset = '\u001b[0m'

def startServer():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	s.listen(3)
	s.setblocking(False)
	entries.append(s)

	return s

def acceptConnection(s):
	ns, address = s.accept()
	generateColor(ns)
	print(f'Conectado com {colors[ns]}{address}{reset}.')

	lock.acquire()
	connections[ns] = address
	lock.release()

	return ns, address

def treatRequests(ns, address):
	while True:
		data = ns.recv(2048)
		if not data: 
			print(f'Encerrado com {colors[ns]}{address}{reset}.')

			lock.acquire()
			del connections[ns]
			lock.release()

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
		print('Não existem conexões ativas.')
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
				t = threading.Thread(target=treatRequests, args=(ns, address))
				t.start()
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

main()
