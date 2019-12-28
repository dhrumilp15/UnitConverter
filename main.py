import os

import sys
from csvConvTable import csvConvTable
from collections import defaultdict
from math import inf

input = sys.stdin.readline

class UnitConverter:
    def __init__(self, filepath_of_csv):
        # Load data
        self.dataHandler = csvConvTable(filename = filepath_of_csv)
        self.dataHandler.loadConvTable()
        
        # Get local copies of rows and fields
        self.rows = self.dataHandler.rows
        self.fields = self.dataHandler.fields
        
        # For total number of nodes in graph
        self.nodes = set()
    
    def main(self, *args): # Driver code
        if len(args) == 0:
            self.getInput()
        else: # To support use from a method call rather than prompting for input
            self.units = args[0]
            self.sourceUnit = args[1]
            self.target = args[2]
        
        self.buildGraph()
        self.bfs(start = self.sourceUnit, target = self.target)
        path = self.getShortestPath(target = self.target)
        self.converted = self.convert(path = path)

    def getInput(self): # To prompt user for input
        print('Welcome to the epic Unit Converter!')
        print('Please format your requested conversion like this:')
        print('[# of source units] [source unit] to [converted unit]')
        print('For example: 1 m to cm')
        
        demand = input().strip().split() # This requires the data to be space-separated
        self.parseInput(demand = demand)
    
    def parseInput(self, demand: str):
        self.units = int(demand[0])
        self.sourceUnit = demand[1]
        self.target = demand[3]

        # Extra checking
        assert(type(self.units) == int)
        assert(type(self.sourceUnit) == str)
        assert(type(self.target) == str)

        # Check if the starting unit and end unit are in the csv at all
        if not (self.sourceUnit in self.dataHandler.getCol('source_unit') or self.target in self.dataHandler.getCol('end_unit')):
            print('Sorry, that conversion isn\'t yet supported')

    def buildGraph(self): # Builds the graph for bfs
        self.graph = defaultdict(list)
        for row in self.rows:
            self.nodes.add(row[1])
            self.nodes.add(row[3])
            self.graph[row[1]].append(row[3])
            self.graph[row[3]].append(row[1]) # to ensure an undirected graph
    
    def loadGraph(self): # To store the graph so that it can save its progress
        pass

    def updateGraph(self, source: str, target: str): # To update the graph so it's better over time
        self.graph[source].append(target)
        self.graph[target].append(source)

    def bfs(self, start : str, target: str): # Performs bfs
        # start = The unit given
        # target = The unit for which conversion is requested
        visited = dict(zip(self.nodes, [False] * len(self.nodes)))
        self.pred = dict(zip(self.nodes, [None] * len(self.nodes))) # To hold references for each unit to its parent
        
        visited[start] = True
        queue = []
        queue.append(start)

        while queue:
            currentUnit = queue.pop(0)
            for unit in self.graph[currentUnit]: # children of currentUnit
                if visited[unit] == False:
                    self.pred[unit] = currentUnit # Ensures that there is only one value in the reference to the parent
                    queue.append(unit)
                    visited[unit] == True
                    if unit == target:
                        return True
        print('This conversion is not yet supported')
        return False
    
    def getShortestPath(self, target: str):
        path = []
        currentUnit = target
        print(self.pred)
        while self.pred[currentUnit] != None:
            path.append(currentUnit)
            currentUnit = self.pred[currentUnit]
            self.updateGraph(source = currentUnit, target = target)
        path.append(currentUnit)
        return path[::-1]

    def convert(self, path: list):
        converted = self.units
        for pathUnit in range(1, len(path)):
            for row in self.rows:
                if path[pathUnit] in row and path[pathUnit - 1] in row:
                    if path[pathUnit] == row[1] and path[pathUnit - 1] == row[3]: # if going from bigger unit to smaller units
                        converted /= float(row[2])
                    elif path[pathUnit] == row[3] and path[pathUnit - 1] == row[1]: # if going from smaller to bigger units
                        converted *= float(row[2])
        return round(converted, 4)
    
    def printFinal(self):
        print('{source_units} {units} = {target_units} {target}'.format(source_units = self.units, units = self.sourceUnit, target_units = self.converted, target = self.target))

biggoMode = UnitConverter(filepath_of_csv = os.getcwd() + '/conversionTable.csv')
biggoMode.main(1, 'cm', 'ft')
biggoMode.printFinal()
