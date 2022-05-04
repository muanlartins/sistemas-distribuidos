import socket
import sys
import select
import threading
import datetime
import glob

# Socket connection info
HOST = ''
PORT = 7776

# Different command entries
entries = [sys.stdin]

# Store socket connections and messages
activeConnections = {}
closedConnections = []
messages = []

# Lock for threading
lock = threading.Lock()

# Variables for coloring on terminal
colors = {}
reset = '\u001b[0m'
red = '\u001b[31m'
colorNumber = 32

def generateColor(ns):
	'''Generate an ANSI escape code to color the terminal according to the node'''
	global colorNumber

	colorPatternStart = '\u001b['
	colorPatternEnd = 'm'

	colors[ns] = colorPatternStart + str(colorNumber) + colorPatternEnd
	colorNumber += 1

def printActiveConnections():
	'''Print all active connections'''
	
	print('')
	if not activeConnections:
		print('There are no active connections.')
	for s in activeConnections:
		print(colors[s] + str(activeConnections[s]) + reset)
	print('')

def printClosedConnections():
	'''Print all closed connections'''

	print('')
	for connection in closedConnections: 
		address, time = connection
		print(address, time)
	print('')

def printMessages():
	'''Print all messages delivered by the server'''

	print('')
	for t in messages: 
		message, address, time = t
		print(red+message+reset, str(address), time)
	print('')

def printHelp():
	'''Print all server commands'''

	print('')
	print(f'{red}h{reset}elp: Of course, otherwise how would you be reading this?!')
	print(f'{red}e{reset}xit: Finish server (only if there are no active connections).')
	print(f'{red}a{reset}ctive: Print all active connections.')
	print(f'{red}c{reset}losed: Print all closed connections.')
	print(f'{red}m{reset}essages: Print all messages transactioned by the server (leave your signature ツ).')	
	print(f'{red}f{reset}iles: Print all files available.')	
	print('')

def printFiles():
	'''Print all files available'''

	print('')
	# Gets all files on folder
	for f in glob.glob("./*.txt"):
		print(f'{red}{str(f)}{reset}')
	print('')

def getFiles():
	'''Return a string containing all files available'''

	files = '\n'

	# Gets all files on folder
	for f in glob.glob("./*.txt"):
		files += f'{red}{str(f)}{reset}\n'

	return files

def getClosedConnections():
	'''Get all closed connections from file'''

	f = open('connections', 'r')
	lines = [line.rstrip() for line in f.readlines()]
	for line in lines:
		address, time = eval(line)
		closedConnections.append((address, time))
	f.close()

def setClosedConnections():
	'''Set all closed connections on file'''

	f = open('connections', 'w')
	for t in closedConnections:
		f.write(str(t)+'\n')
	f.close()

def getMessages():
	'''Get all messages from file'''

	f = open('messages', 'r')
	lines = [line.rstrip() for line in f.readlines()]
	for line in lines:
		message, address, time = eval(line)
		messages.append((message, address, time))
	f.close()

def setMessages():
	'''Set all messages on file'''

	f = open('messages', 'w')
	for m in messages:
		f.write(str(m)+'\n')
	f.close()

def getTime():
	'''Determine the time at the moment for register'''
	return datetime.datetime.now().strftime('%d/%m/%y %X')

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
	activeConnections[ns] = address
	lock.release()

	return ns, address

def treatRequests(ns, address):
	'''Manipulate the data received from the socket, according to the application (echo)'''

	while True:
		msg = ns.recv(2048)
		msg = str(msg, encoding='utf-8')

		# If client closes connection
		if not msg:
			print(f'Closed with {colors[ns]}{address}{reset}.')

			lock.acquire()
			del activeConnections[ns]
			closedConnections.append((address, getTime()))
			lock.release()

			ns.close()
			break
		
		messages.append((msg, address, getTime()))
		print(f'{colors[ns]}{msg}{reset} received from {colors[ns]}{address}{reset}.')

		# If the message is the command 'f'
		if msg == 'f':
			ns.send(bytearray(getFiles(), encoding='utf-8'))
			continue

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
		except:
			erro = f'Arquivo {msg} {red}não encontrado{reset}'
			ns.send(bytearray(erro, encoding='utf-8'))  


def main():
	getClosedConnections()
	getMessages()

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
					if not activeConnections:
						setClosedConnections()
						setMessages()
						s.close()
						sys.exit()
					else:
						print('')
						print(f'{red}There are still active connections{reset}.')
						print('')
				elif cmd == 'h':
					printHelp()
				elif cmd == 'a':
					printActiveConnections()
				elif cmd == 'c':
					printClosedConnections()
				elif cmd == 'm':
					printMessages()
				elif cmd == 'f':
					printFiles()

main()
