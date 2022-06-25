import rpyc
from rpyc.utils.server import ThreadedServer
from random import randint

PORT = 7776

class ProbeEcho(rpyc.Service):
  # RPyC -> node map
  connections = {}

  # All nodes connected
  nodes = []

  # The neighborhood graph (adjacency list)
  neighbors = {}

  # Auxiliar Functions
  def generatePID(self):
    node = randint(1, 50)

    # Avoid repeated PIDs
    while node in self.nodes:
      node = randint(1, 50)

    return node
  
  def addConnection(self, node, conn):
    self.connections[conn] = node
  
  def removeConnection(self, conn):
    return self.connections.pop(conn)

  def addNode(self, node):
    self.nodes.append(node)
  
  def removeNode(self, node):
    self.nodes.remove(node)

  def updateNeighbors(self, node):
    self.neighbors[node] = []

    for neighbor in self.nodes:
      if neighbor != node:

        # 50% chance of having an edge between two nodes
        if randint(0, 1):
          self.neighbors[node].append(neighbor)
          self.neighbors[neighbor].append(node)
    
    print(self.neighbors)
  
  def removeNeighbors(self, node):
    self.neighbors.pop(node, None)
    for key in self.neighbors:
      if node in self.neighbors[key]: self.neighbors[key].remove(node)

  # Depth-first Search for the election algorithm
  def dfs(self, visited, answers, node):
    visited.append(node)
    answers[node] = node

    for neighbor in self.neighbors[node]:
      if neighbor not in visited: 
        answers[node] = max(answers[node], self.dfs(visited, answers, neighbor))

    return answers[node]


  def on_connect(self, conn):
  
    node = self.generatePID()
    self.addConnection(node, conn)
    self.addNode(node)
  
    self.updateNeighbors(node)
    
    print(f"Connection started with process number {node}")    
    # print(self.connections)
    print()
    print(self.nodes)
    print(self.neighbors)
    print()

  def on_disconnect(self, conn):
    node = self.removeConnection(conn)
    self.removeNode(node)
    self.removeNeighbors(node)

    print(self.connections)
    print(self.nodes)
    print(self.neighbors)

    print(f"Connection finished with process number {node}")

    if not self.connections: server.close()
  
  def exposed_getNode(self):
    return self.nodes[-1]
  
  def exposed_startElection(self, node):
    visited = []
    answers = {}
    
    answers[node] = self.dfs(visited, answers, node)

    print(answers)
        
    return answers[node]
    

  
if __name__ == "__main__":
  server = ThreadedServer(ProbeEcho, port=PORT)
  server.start()

