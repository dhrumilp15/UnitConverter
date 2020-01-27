from collections import defaultdict


class graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.nodes = set()

    def buildGraph(self, rows: list):
        '''
            Build an undirected graph from the given nodes

            :param rows: A list of the rows from the conversion table

        '''
        for row in rows:
            self.nodes.add(row[1])
            self.nodes.add(row[3])
            self.graph[row[1]].append(row[3])
            self.graph[row[3]].append(row[1])  # to ensure an undirected graph

    def bfs(self, start: str, target: str) -> bool:
        '''
            Perform Breadth-First Search to find the shortest path in the graph

            :param start: Where in the graph to start
            :param target: The target to find in the graph

            :return: A reference from each node to its parent if it exists
        '''
        if start == target:  # To quickly take care of base case
            return True, {start: None}
        # To hold the nodes already seen, dict so that lookup is easier
        visited = dict(zip(self.nodes, [False] * len(self.nodes)))
        # To hold references for each unit to its parent, dict so that lookup
        # is easier
        parent = dict(zip(self.nodes, [None] * len(self.nodes)))

        visited[start] = True  # Mark the starting node as visited
        queue = []
        queue.append(start)  # Put the starting node on the queue

        while queue:  # Stops if the queue is empty
            currentUnit = queue.pop(0)
            for unit in self.graph[currentUnit]:  # neighbours of currentUnit
                if not visited[unit]:
                    # Ensures that there is only one value in the reference to
                    # the parent
                    parent[unit] = currentUnit
                    queue.append(unit)
                    visited[unit]
                    if unit == target:
                        return True, parent  # return that bfs succeeded and the reference to parent nodes
        return False  # if execution reaches here, bfs failed and the target is disjoint from the start

    def getShortestPath(self, target: str, parent: dict) -> list:
        '''
            From a reference to the parent, retrace steps to get the shortest path

            :param target: A string that is the top parent
            :param parent: A dict of steps to search through

            :return: A list that is the shortest path from the start to the target
        '''
        path = []  # This will store the shortest path
        currentUnit = target

        # Retrace the steps from the reference to parent nodes
        while parent[currentUnit] is not None:
            path.append(currentUnit)
            currentUnit = parent[currentUnit]

        path.append(currentUnit)
        return path[::-1]  # so that the path goes from the start -> target

    def updateGraph(self, source: str, target: str):
        '''
            Update the graph with a source and target

            :param source: The source unit
            :param target: The target unit
        '''
        self.nodes.add(source)
        self.nodes.add(target)
        self.graph[source].append(target)
        self.graph[target].append(source)  # to ensure an undirected graph
