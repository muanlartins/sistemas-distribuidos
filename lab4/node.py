import rpyc
from rpyc.utils.server import ThreadedServer
from random import randint
import os

parent = 0
counter = 0
leader = 0

class Node(rpyc.Service):
  global parent, counter, leader
  port = 0
  identifier = 0
  neighbors = []
  connections = {}

  def on_connect(self, conn):
    global parent, counter, leader

  def on_disconnect(self, conn):
    global parent, counter, leader

  def exposed_introduction(self):
    print(f'\nI am {self.port}')
    print(f'My identifier is {self.identifier}')
    print(f'These are my neighbors: {self.neighbors}')
    print(f'\n{"-"*50}\n')

  def exposed_start(self):
    global parent, counter, leader
    parent = 0
    counter = 0
    leader = 0

    print(f'\n{"*"*80}\n')
    self.exposed_introduction()

    if not self.connections:
      for neighbor in self.neighbors:      
        conn = rpyc.connect('localhost', neighbor)
        conn._config['sync_request_timeout'] = None
        self.connections[neighbor] = conn

  def exposed_startElection(self):
    global parent, counter, leader

    self.exposed_probe(self.port)

  def exposed_probe(self, port):
    global parent, counter, leader

    leader = max(self.identifier, leader)

    if not parent: 
      counter = len(self.neighbors) - 1
      parent = port

      # Leaf
      if not counter and parent != self.port:
        leader = self.identifier
        self.connections[parent].root.echo(leader, self.port)

        print('\nI am a leaf\n')

        return
      
      for neighbor in self.neighbors:
        if neighbor != parent:
          value = self.connections[neighbor].root.probe(self.port)
          if value == 'ACK': 
            print(f'I have received an ACK from {neighbor}\n')
            counter -= 1
            if not counter: 
              print(f'My counter is now {counter}\n')
              if parent != self.port: self.connections[parent].root.echo(leader, self.port)
      
      return

    else: 
      return 'ACK'
  
  def exposed_echo(self, value, son):
    global parent, counter, leader
    if parent != self.port: 
      counter -= 1
    leader = max(value, leader)

    print(f'I have received an ECHO from {son}\n')
    print('Parent: ', parent)
    print('Identifier: ', self.identifier)
    print('Leader: ', leader)
    print()

    if not counter: 
      if parent != self.port: self.connections[parent].root.echo(leader, self.port)


def readPort():
  global parent, counter, leader
  return int('777' + input(""))

def getNeighbors(port):
  global parent, counter, leader
  f = open('graph2.txt', 'r')
  return eval(f.read())[port]

def startNode(node, port):
  global parent, counter, leader
  node.service.port = port
  node.service.identifier = randint(10, 99)
  node.service.neighbors = getNeighbors(port)

  node.service.exposed_introduction(node.service)

def main():
  global parent, counter, leader

  os.system('cls' if os.name == 'nt' else 'clear')

  port = readPort()
  node = ThreadedServer(Node, port=port)

  startNode(node, port)

  node.start()

if __name__ == "__main__":
  main()