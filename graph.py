from collections import defaultdict

class graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.nodes = set()
        
    def buildGraph(self, rows: list):
        for row in rows:
            self.nodes.add(row[1])
            self.nodes.add(row[3])
            self.graph[row[1]].append(row[3])
            self.graph[row[3]].append(row[1]) # to ensure an undirected graph

    def bfs(self, start: str, target: str):
        visited = dict(zip(self.nodes, [False] * len(self.nodes)))
        parent = dict(zip(self.nodes, [None] * len(self.nodes))) # To hold references for each unit to its parent
        
        visited[start] = True
        queue = []
        queue.append(start)

        while queue:
            currentUnit = queue.pop(0)
            for unit in self.graph[currentUnit]: # children of currentUnit
                if visited[unit] == False:
                    parent[unit] = currentUnit # Ensures that there is only one value in the reference to the parent
                    queue.append(unit)
                    visited[unit] == True
                    if unit == target:
                        return True, parent
        print('This conversion is not yet supported')
        return False
    
    def getShortestPath(self, target: str, parent: dict):
        path = [] # This will store the shortest path
        currentUnit = target
        
        while parent[currentUnit] != None:
            path.append(currentUnit)
            currentUnit = parent[currentUnit]
            self.updateGraph(source = currentUnit, target = target) # To make future traversal more efficient
        
        path.append(currentUnit)
        return path[::-1]
    
    def updateGraph(self, source: str, target: str):
        self.nodes.add(source)
        self.nodes.add(target)
        self.graph[source].append(target)
        self.graph[target].append(source) # to ensure an undirected graph
