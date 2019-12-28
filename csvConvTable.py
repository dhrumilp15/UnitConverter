import csv
import os

from conversionTableGetter import conversionTableGetter

class csvConvTable(conversionTableGetter):
    
    def __init__(self, filename):
        self.filename = filename
        self.fields = []
        self.rows = []
    
    def loadConvTable(self):
        with open(self.filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)

            self.parseConvTable(csvreader = csvreader)
    
    def parseConvTable(self, **kwargs):
        csvreader = kwargs['csvreader']
        
        self.fields = next(csvreader) # Assume first row of csv is headings

        for row in csvreader:
           self.rows.append(row) # Add each row to rows
    
    def addToConvTable(self, source: str, target: str, targetUnits: float):
        with open(self.filename, 'a') as csvfile:
            csvfile.write([1, source, targetUnits, target])
    
    def getCol(self, column: str):
        return [row[self.fields.index(column)] for row in self.rows]