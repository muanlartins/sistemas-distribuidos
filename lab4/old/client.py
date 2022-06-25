import rpyc

SERVER = 'localhost'
PORT = 7771

node = 0

def startConnection():
  global node

  conn = rpyc.connect(SERVER, PORT)

  # As soon as it connects, get generated PID
  # node = conn.root.getNode()

  print(node)

  return conn

def closeConnection():
  conn.close()

def main():
  global node

  conn = startConnection()
  while True:
    msg = input("")
    if msg == "ELECTION":
      ret = conn.root.startElection(node)
      print(ret)

    if not msg: break
  conn.close()

if __name__ == "__main__":
  main()