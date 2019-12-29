from unitConverter import UnitConverter
import os

converter = UnitConverter(filepath_of_csv = os.getcwd() + '/conversionTable.csv')
print(converter.main(1, 'm', 'mm'))
print(converter.main(1, 'm', 'in'))
print(converter.main(1, 'm/s', 'in/hr'))