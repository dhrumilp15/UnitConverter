from unitConverter import UnitConverter
import os

converter = UnitConverter(filepath_of_csv = os.getcwd() + '/conversionTable.csv')
converter.main()
converter.printFinal()