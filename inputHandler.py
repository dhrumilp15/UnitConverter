#!/usr/bin/env python3
import sys
from csvConvTable import csvConvTable
from graph import graph

input = sys.stdin.readline # To make getting input from commandline easier in a prompt

class inputHandler():
    def __init__(self, dataHandler: csvConvTable, graph: graph):
        self.dataHandler = dataHandler
        self.graph = graph
    
    def getInput(self) -> list:
        print('Welcome to Dhrumil\'s epic Unit Converter!')
        print('Please format your requested conversion like so:')
        print('[# of source units] [source unit] to [converted unit]')
        print('For example: 1 m to cm')
        flag = True
        while flag: # Checking for valid input
            demand = input().strip().split()
            if len(demand) != 4 or type(demand[1]) != str or type(demand[3]) != str:
                print('That wasn\'t formatted perfectly. Please try again')
            else:
                flag = False
        return demand # This requires the data to be space-separated
    
    def parseInput(self, units: int, sourceUnit: str, target: str) -> list:
        assert(type(units) == int)

        checks = ['/'] # To add more checks if needed
        sourceFlag = any(check in sourceUnit for check in checks)
        endFlag = any(check in target for check in checks)
        
        # if either unit is fractional
        if sourceFlag or endFlag:
            
            # if the source and target units are in the csv, conversion while remaining in fractional form may be possible
            if sourceUnit in self.dataHandler.getCol(column= 'source_unit') and target in self.dataHandler.getCol(column = 'end_unit'):
                conversions = [(sourceUnit, target)]

            # if the fractional units don't exist in the csv and BOTH start and target units are fractional
            elif sourceFlag and endFlag:
                sourceUnit = sourceUnit.split('/')
                target = target.split('/')
                conversions = list(zip(sourceUnit, target))
            
            else:
                if sourceFlag:
                    frac,nonfrac = sourceUnit, target
                else:
                    frac,nonfrac = target,sourceUnit
                for neighbour in self.graph.graph[nonfrac]:
                    if any(check in neighbour for check in checks):
                        frac = frac.split('/')
                        nonfrac = neighbour.split('/')
                        conversions = list(zip(frac, nonfrac)) if sourceFlag else list(zip(nonfrac,frac))
                        units *= self.dataHandler.convert(path = [frac, nonfrac]) if sourceFlag else self.dataHandler.convert(path = [nonfrac, frac])
                        break
        else:
            conversions = [(sourceUnit, target)]
        
        for conversion in conversions:
            # Extra checking
            assert(isinstance(conversion[0],str))
            assert(isinstance(conversion[1],str))         
            
            # Check if the starting unit and end unit are in the csv at all
            if not (any(conv in self.dataHandler.getCol('source_unit') for conv in conversion) or any(conv in self.dataHandler.getCol('end_unit') for conv in conversion)):
                print('Sorry, that conversion isn\'t yet supported')
                sys.exit(-1)
        return units, conversions