#!/usr/bin/env python3
from UnitConverter import UnitConverter
import os

# Sample Driver Code

converter = UnitConverter(filepath_of_csv = os.getcwd() + '/conversionTable.csv')
converter.main(3.5, 'm', 'in')
converter.printFinal()