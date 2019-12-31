from csvConvTable import csvConvTable

import os
import pytest
csvHandler = csvConvTable()

def load_csv(filepath: str):
    csvHandler.loadConvTable(filepath)

def test_bad_csv_path(): # Tests if the csv given doesn't exist
    with pytest.raises(FileNotFoundError):
        load_csv('sickoMode')

def test_get_col():
    assert(isinstance(csvHandler.getCol(column = 'source_unit'), list))
    assert(isinstance(csvHandler.getCol(column = 'number_of_source_units'), list))
    assert(isinstance(csvHandler.getCol(column = 'end_unit'), list))
    assert(isinstance(csvHandler.getCol(column = 'number_of_end_units'), list))

def test_get_rows():
    assert(isinstance(csvHandler.getRows(), list))

def test_get_fields():
    assert(isinstance(csvHandler.getFields(), list))