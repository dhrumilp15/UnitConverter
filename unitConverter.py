import sys, logging
from csvConvTable import csvConvTable
from graph import graph
from inputHandler import inputHandler

input = sys.stdin.readline # To make getting input faster
logging.basicConfig(stream = sys.stderr, level = logging.DEBUG)

class UnitConverter:
    def __init__(self, filepath_of_csv: str):
        # Load data
        self.dataHandler = csvConvTable()
        self.dataHandler.loadConvTable(filename = filepath_of_csv)
        
        # Get a local copy of the rows
        self.rows = self.dataHandler.getRows()
        
        # Build Graph
        self.graph = graph()
        self.graph.buildGraph(self.rows)

        # Get an inputHandler object
        self.inputHandler = inputHandler(self.dataHandler, self.graph)
        
        # Holds the final result of conversion
        self.converted = []

    def main(self, *args) -> float:
        # Clear any previous results
        self.converted = []
        self.conversions = []

        # Get Input
        if len(args) == 0: # Prompting for input
            demand = self.inputHandler.getInput()
            self.originalUnits = demand[0]
            self.sourceUnit = demand[1]
            self.target = demand[3]
            self.units, self.conversions = self.inputHandler.parseInput(units = int(self.originalUnits), sourceUnit = self.sourceUnit, target = self.target)
        
        elif len(sys.argv) > 1: # To support commandline use
            self.originalUnits = sys.argv[1]
            self.sourceUnit = sys.argv[2]
            self.target = sys.argv[3]
            self.units, self.conversions = self.inputHandler.parseInput(units = int(self.originalUnits), sourceUnit = self.sourceUnit, target = self.target)
        
        else: # To support use from a method call
            self.originalUnits = args[0]
            self.sourceUnit = args[1]
            self.target = args[2]
            self.units, self.conversions = self.inputHandler.parseInput(units = self.originalUnits, sourceUnit = self.sourceUnit, target = self.target)
        
        for index, conversion in enumerate(self.conversions): # Perform conversions for both numerator and denominator
            # Searching and path finding needs to be done for each conversion
            bfsres = self.graph.bfs(start = conversion[0], target = conversion[1])
            
            # Only if there's a possible way to get from the source to the target
            if bfsres:
                path = self.graph.getShortestPath(target = conversion[1], parent = bfsres[1])
                convertUnits = self.dataHandler.convert(path = path, units = 1) if index else self.dataHandler.convert(path = path, units = self.units)
                self.converted.append(convertUnits)
                if len(self.converted) > 1: # To yield just numbers from main()
                    self.target_units = round(self.converted[0] / self.converted[1], 4) # If it's a complex conversion, divide the numerator by the denominator
                else:
                    self.target_units = round(self.converted[0], 4)
            else:
                print('This conversion can\'t be completed')
                return
        return self.target_units

    def convert(self, path: list, index: int = 1) -> float:
        converted = 1 if index else self.units # only apply multiply the number of units with the numerator
        for pathUnit in range(1, len(path)):
            for row in self.rows:
                if path[pathUnit] in row and path[pathUnit - 1] in row:
                    if path[pathUnit] == row[1] and path[pathUnit - 1] == row[3]: # if going from bigger unit to smaller units
                        converted /= float(row[2])
                    elif path[pathUnit] == row[3] and path[pathUnit - 1] == row[1]: # if going from smaller to bigger units
                        converted *= float(row[2])
        return converted
    
    def printFinal(self):
        print('{source_units} {units} = {target_units} {target}'.format(source_units = self.originalUnits, units = self.sourceUnit, target_units = self.target_units, target = self.target))