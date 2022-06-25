import rpyc
import time

SERVER = 'localhost'
ports = [7770, 7771, 7772, 7773, 7774]

def startConnection(port):
  conn = rpyc.connect(SERVER, port)
  return conn

def closeConnection(conn):
  conn.close()

def main():
  global ports

  while True:
    for port in ports:
      conn = startConnection(port)
      conn.root.start()
      conn.close()


    port = int("777" + input(""))
    conn = startConnection(port)
    conn._config['sync_request_timeout'] = None
    conn.root.startElection()
    closeConnection(conn)

if __name__ == "__main__":
  main()