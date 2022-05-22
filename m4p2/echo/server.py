import rpyc

# Processo Filho
from rpyc.utils.server import ForkingServer

# Thread
from rpyc.utils.server import ThreadedServer

# Uma conexão e termina
from rpyc.utils.server import OneShotServer

PORT = 7776

class Echo(rpyc.Service):
  def on_connect(self, conn):
    print("Connection started")
  def on_disconnect(self, conn):
    print("Connection finished")
  def exposed_echo(self, msg):
    print(msg)
    return msg

class Calculator(rpyc.Service):
  connections = 0

  def on_connect(self, conn):
    print("Connection started")
    connections += 1
  def on_disconnect(self, conn):
    print("Connection finished")
    connections -= 1
    if not connections: serverCalculator.close()
  def exposed_sum(self, a, b):
    print('Sum ', a, '+', b, '=', a + b)
    return a+b
  def exposed_difference(self, a, b):
    print('Difference ', a, '-', b, '=', a - b)
    return a-b
  def exposed_product(self, a, b):
    print('Product ', a, '*', b, '=', a * b)
    return a*b
  def exposed_division(self, a, b):
    print('Division ', a, '/', b, '=', a / b)
    return a/b
  


if __name__ == "__main__":
  serverEcho = ForkingServer(Echo, port=PORT)
  serverCalculator = ThreadedServer(Calculator, port=PORT)
  # serverEcho.start()
  serverCalculator.start()
