from unitConverter import UnitConverter
import os

biggoMode = UnitConverter(filepath_of_csv = os.getcwd() + '/conversionTable.csv')
biggoMode.main(1, 'm/hr', 'in/s')
biggoMode.printFinal()