from __future__ import with_statement
import csv
import os

from conversionTableGetter import conversionTableGetter

class csvConvTable(conversionTableGetter):
    
    def __init__(self):
        self.rows = []
        self.fields = []
    
    def loadConvTable(self, filename: str): # Try to load the csv file
        try:
            with open(filename, 'r') as csvfile:
                csvreader = csv.reader(csvfile)

                self.parseConvTable(csvreader = csvreader)
        except Exception:
            raise FileNotFoundError
    
    def parseConvTable(self, **kwargs): # Technically a helper method
        csvreader = kwargs['csvreader']
        
        self.fields = next(csvreader) # Assume first row of csv is headings

        for row in csvreader:
           self.rows.append(row) # Add each row to rows
    
    def addToConvTable(self, source: str, target: str, targetUnits: float):
        with open(self.filename, 'a') as csvfile:
            csvfile.write([1, source, targetUnits, target])
    
    def getCol(self, column: str) -> list: # Helper method
        return [row[self.fields.index(column)] for row in self.rows]
    
    def getRows(self) -> list: # Getter method for rows
        return self.rows
    
    def getFields(self) -> list: # Getter method for fields
        return self.fields