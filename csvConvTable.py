#!/usr/bin/env python3
from __future__ import with_statement
import csv
import os

from conversionTableGetter import conversionTableGetter

class csvConvTable(conversionTableGetter):
    
    def __init__(self):
        self.rows = []
        self.fields = []
    
    def loadConvTable(self, filename: str) -> None: # Try to load the csv file
        '''
            Load a conversion table from the given filename
        '''
        try:
            with open(filename, 'r') as csvfile:
                csvreader = csv.reader(csvfile)

                self.parseConvTable(csvreader = csvreader)
        except Exception:
            raise FileNotFoundError
    
    def parseConvTable(self, **kwargs) -> None: # Technically a helper method
        '''
            Parse the conversion table to update class variables to the rows in the table
        '''
        csvreader = kwargs['csvreader']
        
        self.fields = next(csvreader) # Assume first row of csv is headings

        for row in csvreader:
           self.rows.append(row) # Add each row to rows
    
    def addToConvTable(self, source: str, target: str, targetUnits: float):
        with open(self.filename, 'a') as csvfile:
            csvfile.write([1, source, targetUnits, target])
    
    def getCol(self, column: str) -> list: # Helper method
        '''
        Gets a column from the csv conversion Table

        :return: List of the given column from the csv conversion Table
        '''
        return [row[self.fields.index(column)] for row in self.rows]
    
    def getRows(self) -> list: # Getter method for rows
        '''
        Gets a row from the csv conversion Table

        :return: List of the given row from the csv conversion Table
        '''
        return self.rows
    
    def getFields(self) -> list: # Getter method for fields
        '''
        Gets fields from the csv conversion Table

        :return: List of the fields in the csv conversion Table
        '''
        return self.fields
    
    def convert(self, path, units = 1):
        '''
        Convert along the path

        :return: List of the given column from the csv conversion Table
        '''
        converted = units
        for pathUnit in range(1, len(path)):
            for row in self.rows:
                if path[pathUnit] in row and path[pathUnit - 1] in row:
                    if path[pathUnit] == row[1] and path[pathUnit - 1] == row[3]: # if going from bigger unit to smaller units
                        converted /= float(row[2])
                    elif path[pathUnit] == row[3] and path[pathUnit - 1] == row[1]: # if going from smaller to bigger units
                        converted *= float(row[2])
        return converted