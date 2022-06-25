import json, rpyc
from rpyc.utils.server import OneShotServer
from random import randint

SERVER = 'localhost'
PORT = 0
STARTER = 7770

graph = {}
maxCapacity = 0
maxCapacityOwner = PORT
visited = {}

class Node(rpyc.Service):
  def on_connect(self, conn):
    print(f'{PORT}: Connected')
  
  def on_disconnect(self, conn):
    print(f'{PORT}: Disconnected')
  
  def exposed_getCapacity(self, visitedByNeighbor):
    global maxCapacity, maxCapacityOwner

    capacity = randint(1, 50)

    mergeVisits(visitedByNeighbor)
    visitNeighbors()

    print(f'{PORT}: capacity is {capacity}')
    print(f'{PORT}: maxCapacity is {maxCapacity}')
    print(f'{PORT}: maxCapacityOwner is {maxCapacityOwner}')

    if (capacity > maxCapacity):
      maxCapacity = capacity
      maxCapacityOwner = PORT

    return (maxCapacity, maxCapacityOwner, visited)


def readFile():
  global graph

  f = open("graph.txt", "r")
  graph = eval(f.read())

  for port in graph:
    visited[port] = False
  
  visited[STARTER] = True

def createServer():
  server = OneShotServer(Node, port=PORT)
  server.start()

def readPort():
  global PORT

  PORT = int('777' + input(""))

def mergeVisits(visitedByNeighbor):
  global visited

  for neighbor in visitedByNeighbor:
      visited[neighbor] = visited[neighbor] or visitedByNeighbor[neighbor]

def visitNeighbors():
  global PORT, maxCapacity, maxCapacityOwner, graph, visited

  neighbors = graph[PORT]
  for neighbor in neighbors:
    if visited[neighbor]: continue
    visited[neighbor] = True
    conn = rpyc.connect(SERVER, neighbor)
    capacity, capacityOwner, visitedByNeighbor = conn.root.getCapacity(visited)

    if (capacity > maxCapacity):
      maxCapacity = capacity
      maxCapacityOwner = capacityOwner
    mergeVisits(visitedByNeighbor)

def simulateElection():
  global PORT, STARTER, maxCapacity

  if PORT != STARTER: createServer()
  else: visitNeighbors()

  print(maxCapacity)

    

def main():
  readFile()
  readPort()
  simulateElection()
  

if __name__ == "__main__":
  main()