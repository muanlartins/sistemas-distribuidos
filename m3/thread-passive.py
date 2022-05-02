import socket
import sys
import select
import threading

# Socket connection info
HOST = ''
PORT = 7776

# Different command entries
entries = [sys.stdin]

# Store socket connections
connections = {}

# Lock for threading
lock = threading.Lock()

# Variables for coloring on terminal
colors = {}
reset = '\u001b[0m'
red = '\u001b[31m'

def generateColor(ns):
	'''Generate an ANSI escape code to color the terminal according to the node'''
	colorPatternStart = '\u001b['
	colorPatternEnd = 'm'
	colorNumber = 32

	colors[ns] = colorPatternStart + str(colorNumber) + colorPatternEnd
	colorNumber += 1

def printConnections():
	'''Print all connections'''
	if not connections:
		print('There are no active connections.')
	for entry in connections.keys():
		print(colors[entry] + str(connections[entry]) + reset)

def startServer():
	'''Create a new socket, binding it to the HOST and PORT'''

	s = socket.socket()
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	s.listen(3)
	s.setblocking(False)
	entries.append(s)

	return s

def acceptConnection(s):
	'''Accept connection with a socket'''

	ns, address = s.accept()
	generateColor(ns)
	print(f'Connected with {colors[ns]}{address}{reset}.')

	lock.acquire()
	connections[ns] = address
	lock.release()

	return ns, address

def treatRequests(ns, address):
	'''Manipulate the data received from the socket, according to the application (echo)'''

	while True:
		data = ns.recv(2048)
		if not data: 
			print(f'Closed with {colors[ns]}{address}{reset}.')

			lock.acquire()
			del connections[ns]
			lock.release()

			ns.close()
			return
		print(f'{colors[ns]}{str(data, encoding="utf-8")}{reset} received from {colors[ns]}{address}{reset}.')
		ns.send(data)

def main():
	s = startServer()
	print('Server started.')
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
						print(f'{red}Ainda existem conexões ativas{reset}.')
				elif cmd == 'h':
					printConnections()

main()
