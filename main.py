from unitConverter import UnitConverter
import os

converter = UnitConverter(filepath_of_csv = os.getcwd() + '/conversionTable.csv')
converter.main(1, 'm', 'mm')
converter.printFinal()

converter.main(1, 'm', 'in')
converter.printFinal()

converter.main(1, 'm/s', 'in/hr')
converter.printFinal()

converter.main(1, 'W', 'kJ/hr')
converter.printFinal()

converter.main(1, 'kJ/hr', 'W')
converter.printFinal()