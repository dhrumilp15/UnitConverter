from collections import defaultdict

class graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.nodes = set()
        
    def buildGraph(self, rows: list) -> None:
        '''
            Build an undirected graph from the given nodes

            @params
            rows: A list of the rows from the conversion table
            
        '''
        for row in rows:
            self.nodes.add(row[1])
            self.nodes.add(row[3])
            self.graph[row[1]].append(row[3])
            self.graph[row[3]].append(row[1]) # to ensure an undirected graph

    def bfs(self, start: str, target: str) -> bool:
        '''
            Perform Breadth-First Search to find the shortest path in the graph
            
            @params
            start: Where in the graph to start
            target: The target to find in the graph

            If a path exists, return a reference from each node to its parent
        '''
        if start == target: # To quickly take care of base case
            return True, {start: None}
        visited = dict(zip(self.nodes, [False] * len(self.nodes))) # To hold the nodes already seen, dict so that lookup is easier
        parent = dict(zip(self.nodes, [None] * len(self.nodes))) # To hold references for each unit to its parent, dict so that lookup is easier
        
        visited[start] = True # Mark the starting node as visited
        queue = []
        queue.append(start) # Put the starting node on the queue

        while queue: # Stops if the queue is empty
            currentUnit = queue.pop(0)
            for unit in self.graph[currentUnit]: # neighbours of currentUnit
                if visited[unit] == False:
                    parent[unit] = currentUnit # Ensures that there is only one value in the reference to the parent
                    queue.append(unit)
                    visited[unit] == True
                    if unit == target:
                        return True, parent # return that bfs succeeded and the reference to parent nodes
        return False # if execution reaches here, bfs failed and the target is disjoint from the start
    
    def getShortestPath(self, target: str, parent: dict) -> list:
        '''
            From a reference to the parent, retrace steps to get the shortest path

            @params
            target: A string that is the top parent
            parent: A dict of steps to search through

            return a list that is the shortest path from the start to the target
        '''
        path = [] # This will store the shortest path
        currentUnit = target
        
        while parent[currentUnit] != None: # Retrace the steps from the reference to parent nodes
            path.append(currentUnit)
            currentUnit = parent[currentUnit]
        
        path.append(currentUnit)
        return path[::-1] # so that the path goes from the start -> target
    
    def updateGraph(self, source: str, target: str)-> None:
        '''
            Update the graph with a source and target

            @params:
            source: The source unit
            target: The target unit
        '''
        self.nodes.add(source)
        self.nodes.add(target)
        self.graph[source].append(target)
        self.graph[target].append(source) # to ensure an undirected graph