#!/usr/bin/env python3
import sys
import os
import argparse

from csvConvTable import csvConvTable
from graph import graph
from inputHandler import inputHandler

input = sys.stdin.readline  # To make getting input faster


class UnitConverter:
    def __init__(self, filepath_of_csv: str):

        # Load data
        self.dataHandler = csvConvTable()
        self.dataHandler.loadConvTable(filename=filepath_of_csv)

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

        if len(args) == 0:  # Prompting for input
            demand = self.inputHandler.getInput()
            self.originalUnits = demand[0]
            self.sourceUnit = demand[1]
            self.target = demand[3]
            self.units, self.conversions = self.inputHandler.parseInput(units=float(
                self.originalUnits), sourceUnit=self.sourceUnit, target=self.target)

        else:  # To support use from a method call
            self.originalUnits = args[0]
            self.sourceUnit = args[1]
            self.target = args[2]
            self.units, self.conversions = self.inputHandler.parseInput(
                units=self.originalUnits, sourceUnit=self.sourceUnit, target=self.target)

        for index, conversion in enumerate(
                self.conversions):  # Perform conversions for both numerator and denominator
            # Searching and path finding needs to be done for each conversion
            bfsres = self.graph.bfs(start=conversion[0], target=conversion[1])

            # Convert only if there's a possible way to get from the source to
            # the target
            if bfsres:
                path = self.graph.getShortestPath(
                    target=conversion[1], parent=bfsres[1])
                convertUnits = self.dataHandler.convert(
                    path=path, units=1) if index else self.dataHandler.convert(
                    path=path, units=self.units)
                self.converted.append(convertUnits)
                if len(self.converted) > 1:  # To yield just numbers from main()
                    # If it's a complex conversion, divide the numerator by the
                    # denominator
                    self.target_units = round(
                        self.converted[0] / self.converted[1], 4)
                else:
                    self.target_units = round(self.converted[0], 4)
            else:
                print('This conversion can\'t be completed')
                return
        return self.target_units


    def printFinal(self):
        '''
            Print the final result of conversion
        '''
        print(
            '{source_units} {units} = {target_units} {target}'.format(
                source_units=self.originalUnits,
                units=self.sourceUnit,
                target_units=self.target_units,
                target=self.target))


if __name__ == "__main__":
    '''
    Argument Parser if this file is called directly
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "units",
        nargs='?',
        type=float,
        default=1.0,
        help='Number of start units')
    parser.add_argument(
        "start",
        nargs='?',
        type=str,
        default=None,
        help='Type of start unit')
    parser.add_argument(
        "target",
        nargs='?',
        type=str,
        default=None,
        help='Type of target unit')
    parser.add_argument(
        "-cv",
        "--convTable",
        type=str,
        default=os.path.join(
            os.getcwd(),
            'conversionTable.csv'),
        help='Filepath for conversion table')
    args = parser.parse_args()

    unit_converter = UnitConverter(args.convTable)

    if args.start and args.target:
        unit_converter.main(args.units, args.start, args.target)
    else:
        unit_converter.main()
    unit_converter.printFinal()
