import sys
from csvConvTable import csvConvTable
from graph import graph

input = sys.stdin.readline

class UnitConverter:
    def __init__(self, filepath_of_csv):
        # Load data
        self.dataHandler = csvConvTable(filename = filepath_of_csv)
        self.dataHandler.loadConvTable()
        
        # Get local copies of rows and fields
        self.rows = self.dataHandler.rows
        self.fields = self.dataHandler.fields

        self.converted = []
    
    def main(self, *args): # Driver code
        if len(args) == 0: # Prompting for input
            self.getInput()
        elif len(sys.argv) > 1: # To support commandline use
            self.parseInput(units = int(sys.argv[1]), sourceUnit=sys.argv[2], target = sys.argv[3])
        else: # To support use from a method call
            self.parseInput(units = args[0], sourceUnit=args[1], target = args[2])
        
        self.graph = graph()
        self.graph.buildGraph(self.rows)
        
        for conversion in self.conversions:
            bfsres = self.graph.bfs(start = conversion[0], target = conversion[1])
            if bfsres:
                path = self.graph.getShortestPath(target = conversion[1], parent = bfsres[1])
                self.converted.append(self.convert(path = path))

    def getInput(self): # To prompt user for input
        print('-' * 20)
        print('Welcome to the epic Unit Converter!')
        print('Please format your requested conversion like this:')
        print('[# of source units] [source unit] to [converted unit]')
        print('For example: 1 m to cm')
        
        demand = input().strip().split() # This requires the data to be space-separated
        self.parseInput(units = int(demand[0]), sourceUnit = demand[1], target = demand[3])
    
    def parseInput(self, units: int, sourceUnit: str, target: str):
        self.sourceUnit = sourceUnit
        self.target = target
        
        checks = ['/', '^-1']
        if any(check in sourceUnit for check in checks) or any(check in target for check in checks):
            sourceUnit = sourceUnit.split('/')
            target = target.split('/')
            self.conversions = list(zip(sourceUnit, target))
        else:
            self.conversions = [(sourceUnit, target)]
        
        self.units = units
        assert(type(self.units) == int)
        
        for conversion in self.conversions:

          assert(type(conversion[0]) == str)
          assert(type(conversion[1]) == str)
          
          # Check if the starting unit and end unit are in the csv at all
          if not (conversion[0] in self.dataHandler.getCol('source_unit') or conversion[1] in self.dataHandler.getCol('end_unit')):
              print('Sorry, that conversion isn\'t yet supported')
              sys.exit(-1)

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
        if len(self.converted) > 1:
            value = round(self.converted[0] / self.converted[1], 4)
        else:
            value = converted[0]
        print('{source_units} {units} = {target_units} {target}'.format(source_units = self.units, units = self.sourceUnit, target_units = value, target = self.target))