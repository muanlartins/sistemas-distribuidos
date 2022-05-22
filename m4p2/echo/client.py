import rpyc

SERVER = 'localhost'
PORT = 7776

def startConnection():
  conn = rpyc.connect(SERVER, PORT)

  return conn

def makeRequestsEcho(conn):
  while True:
    msg = input('')
    if not msg: break

    ret = conn.root.echo(msg)

    print(ret)

  conn.close()

def makeRequestsCalculator(conn):
  while True:
    msg = input('')
    if not msg: break

    a, o, b = msg.split()

    a, b = int(a), int(b)

    if o == '+': ret = conn.root.sum(a, b)
    if o == '-': ret = conn.root.difference(a, b)
    if o == '*': ret = conn.root.product(a, b)
    if o == '/': ret = conn.root.division(a, b)

    print(ret)

  conn.close()

def main():
  conn = startConnection()
  # makeRequestsEcho(conn)
  makeRequestsCalculator(conn)

if __name__ == "__main__":
  main()
