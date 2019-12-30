from unitConverter import UnitConverter

import pytest
import os

# This tests whether the unit converter produces the correct output

unitConverter = UnitConverter(os.getcwd() + '/conversionTable.csv')

def test_converter_on_sample_conversions():
    # Basic Conversions
    assert(unitConverter.main(0, 'm', 'mm')) == 0
    assert(unitConverter.main(1, 'm', 'mm')) == 1000
    assert(unitConverter.main(1, 'm', 'in')) == 39.3701
    assert(unitConverter.main(1, 'ft', 'cm')) == 30.48
    assert(unitConverter.main(10, 'ft', 'cm')) == 304.8
    assert(unitConverter.main(1, 'mm', 'in')) == 0.0394
    assert(unitConverter.main(3, 'cm', 'm')) == 0.03

    # Complex conversions
    assert(unitConverter.main(1, 'm/s', 'in/hr')) == 141732.2835
    assert(unitConverter.main(1, 'mm/s', 'cm/hr')) == 360

    # Combined complex conversions
    assert(unitConverter.main(1, 'W', 'kJ/hr')) == 3.6
    assert(unitConverter.main(1, 'kJ/hr', 'W')) == 0.2778
    assert(unitConverter.main(1, 'W', 'kJ/s')) == 0.001
    assert(unitConverter.main(1, 'kJ/s', 'W')) == 1000
    assert(unitConverter.main(2, 'kJ/s', 'W')) == 2000

def test_parse_input():
    # Basic input:
    assert(unitConverter.parseInput(1,'m','mm')) == [('m','mm')]
    
    # Complex input
    assert(unitConverter.parseInput(1,'m/s','in/hr')) == [('m','in'), ('s', 'hr')]
    
    # Combined Complex Input
    assert(unitConverter.parseInput(1,'W','kJ/s')) == [('J','kJ'), ('s', 's')]