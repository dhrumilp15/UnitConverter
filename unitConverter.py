import sys, logging
from csvConvTable import csvConvTable
from graph import graph

input = sys.stdin.readline # To make getting input faster
logging.basicConfig(stream = sys.stderr, level = logging.DEBUG)

class UnitConverter:
    def __init__(self, filepath_of_csv: str):
        # Load data
        self.dataHandler = csvConvTable()
        self.dataHandler.loadConvTable(filename = filepath_of_csv)
        
        # Get a local copy of the rows
        self.rows = self.dataHandler.getRows()

        # Holds the final result of conversion
        self.converted = []
    
    def main(self, *args) -> float:
        # Clear any previous results
        self.converted = []
        self.conversions = []

        self.graph = graph() # Get graph object
        self.graph.buildGraph(self.rows) # Populate graph

        if len(args) == 0: # Prompting for input
            demand = self.getInput()
            self.parseInput(units = int(demand[0]), sourceUnit = demand[1], target = demand[3])
        elif len(sys.argv) > 1: # To support commandline use
            self.parseInput(units = int(sys.argv[1]), sourceUnit=sys.argv[2], target = sys.argv[3])
        else: # To support use from a method call
            self.parseInput(units = args[0], sourceUnit=args[1], target = args[2])
        
        for index, conversion in enumerate(self.conversions): # Perform conversions for both numerator and denominator
            # Searching and path finding needs to be done for each conversion
            bfsres = self.graph.bfs(start = conversion[0], target = conversion[1])
            
            # Only if there's a possible way to get from the source to the target
            if bfsres:
                path = self.graph.getShortestPath(target = conversion[1], parent = bfsres[1])
                self.converted.append(self.convert(path = path, index = index))
                if len(self.converted) > 1: # To yield just numbers from main()
                    self.target_units = round(self.converted[0] / self.converted[1], 4) # If it's a complex conversion, divide the numerator by the denominator
                else:
                    self.target_units = round(self.converted[0], 4)
            else:
                print('This conversion can\'t be completed')
                return
        return self.target_units

    def getInput(self) -> list: # To prompt user for input
        print('Welcome to Dhrumil\'s epic Unit Converter!')
        print('Please format your requested conversion like so:')
        print('[# of source units] [source unit] to [converted unit]')
        print('For example: 1 m to cm')
        flag = True
        while flag: # Checking for valid input
            demand = input().strip().split()
            if len(demand) != 4 or type(demand[1]) != str or type(demand[3]) != str:
                print('That wasn\'t formatted perfectly. Try again')
            else:
                flag = False
        return demand # This requires the data to be space-separated
    
    def parseInput(self, units: int, sourceUnit: str, target: str):
        self.sourceUnit = sourceUnit
        self.target = target
        self.originalUnits = units
        self.units = units; assert(type(self.units) == int)

        checks = ['/'] # To add more checks if needed
        sourceFlag = any(check in sourceUnit for check in checks)
        endFlag = any(check in target for check in checks)
        
        # if either unit is fractional
        if sourceFlag or endFlag:
            
            # if the source and target units are in the csv, conversion while remaining in fractional form may be possible
            if sourceUnit in self.dataHandler.getCol(column= 'source_unit') and target in self.dataHandler.getCol(column = 'end_unit'):
                self.conversions = [(sourceUnit, target)]
                
            
            # if only the source unit is fractional: kj/hr -> W
            elif sourceFlag and not endFlag:
                for neighbour in self.graph.graph[target]:
                    if any(check in neighbour for check in checks):
                        sourceUnit = sourceUnit.split('/') # ASSUMPTION: There exists a path from the first neighbour it finds to the source
                        target = neighbour.split('/')
                        self.conversions = list(zip(sourceUnit, target))
                        break
            
            # if only the end unit is fractional: W -> kJ/hr
            elif endFlag and not sourceFlag:
                for neighbour in self.graph.graph[sourceUnit]:
                    if any(check in neighbour for check in checks):
                        target = target.split('/') # ASSUMPTION: There exists a path from the first neighbour it finds to the target
                        sourceUnit = neighbour.split('/')
                        self.conversions = list(zip(sourceUnit, target))
                        self.units *= self.convert(path = [sourceUnit, neighbour])
                        break
                    
            # if the fractional units don't exist in the csv and BOTH start and target units are fractional
            else:
                sourceUnit = sourceUnit.split('/')
                target = target.split('/')
                self.conversions = list(zip(sourceUnit, target))
        else:
            self.conversions = [(sourceUnit, target)]
        
        for conversion in self.conversions:
            # Extra checking
            assert(isinstance(conversion[0],str))
            assert(isinstance(conversion[1],str))         
            
            # Check if the starting unit and end unit are in the csv at all
            if not (any(conv in self.dataHandler.getCol('source_unit') for conv in conversion) or any(conv in self.dataHandler.getCol('end_unit') for conv in conversion)):
                print('Sorry, that conversion isn\'t yet supported')
                sys.exit(-1)
        return self.conversions

    def convert(self, path: list, index: int = 1) -> float:
        converted = 1 if index else self.units # only apply units multiplication on the numerator
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