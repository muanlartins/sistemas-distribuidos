import rpyc, os, threading
from rpyc.utils.server import ThreadedServer

SERVER = 'localhost'
PORT = 0
neighbors = ['7771', '7772', '7773', '7774']
primaryCopy = '7771'

Id = 0
X = 0
changesHistory = []

# ANSI escape code to color terminal
def esc(code):
  return f'\033[{code}m'

# Turns the message red
def red(message):
  return f"{esc(31)}{message}{esc(0)}"

# Clear terminal
def clear():
  os.system('cls' if os.name == 'nt' else 'clear')

def sleep():
  print()
  input("Press enter to choose another option")

# Read the option
def read():
  clear()

  print("Welcome! Choose your option:\n")
  print(f"1. Read the value of {red('X')}")
  print(f"2. Read changes history of {red('X')}")
  print(f"3. Change the value of {red('X')}")
  print(f"{red('4. Finish the program')}")
  print(f"5. Read the primary copy\n")
  
  return int(input(""))

# Read the value of X
def readValue():
  clear()

  print(f"This is the value of X: {red(X)}")

  sleep()

# Read changes history
def readChangesHistory():
  clear()

  for change in changesHistory:
    print(change)

  sleep()

def addChange():
  changesHistory.append((Id, X))

def getPermissionToWrite():
  global primaryCopy

  conn = rpyc.connect('localhost', primaryCopy)
  newPort = conn.root.getPermissionToWrite(PORT)
  while newPort:
    newConn = rpyc.connect('localhost', newPort)
    newPort = newConn.root.getPermissionToWrite(PORT)
    newConn.close()

  primaryCopy = PORT

  conn.close()

def sendXToOtherNodes():
  for neighbor in neighbors:
    if neighbor != PORT:
      conn = rpyc.connect('localhost', neighbor)
      conn.root.updateX(X)
      conn.close()

def changeValue():
  global X

  clear()

  newX = int(input("Enter the new value of X: "))
  if primaryCopy != PORT: getPermissionToWrite()
  X = newX
  addChange()
  sendXToOtherNodes()

# Read node's Id
def readId():
  global Id, PORT, primaryCopy

  clear()

  Id = int(input("Type this node's Id: "))

  PORT = "777"+str(Id)

class Node(rpyc.Service):
  # def on_connect(self, conn):
  # def on_disconnect(self, conn):

  def exposed_getPermissionToWrite(self, port):
    global primaryCopy

    # I'm not the primary copy
    if primaryCopy != PORT:
      primaryCopyTemp = primaryCopy
      primaryCopy = port
      return primaryCopyTemp
    
    else:
      primaryCopy = port
      for neighbor in neighbors:
        if neighbor != PORT:
          conn = rpyc.connect('localhost', neighbor)
          conn.root.addChange(changesHistory[-1])
          conn.close()

  
  def exposed_updateX(self, newX):
    global X

    X = newX

  def exposed_addChange(self, change):
    global changesHistory

    changesHistory.append(change)

def startServer():
  node = ThreadedServer(Node, port=PORT)
  node.start()

def printVariables():
  clear()

  print(f'primaryCopy: {primaryCopy}')

  sleep()

def main():
  readId()
  server = threading.Thread(target=startServer)
  server.start()
  while True:
    option = read()
    if option == 1:
      readValue()
    elif option == 2:
      readChangesHistory()
    elif option == 3:
      changeValue()
    elif option == 4:
      clear()
      os._exit(0)
    elif option == 5:
      printVariables()
    else:
      continue

if __name__ == "__main__":
  main()