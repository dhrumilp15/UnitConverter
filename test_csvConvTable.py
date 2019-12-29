from csvConvTable import csvConvTable

import os
import pytest
csvHandler = csvConvTable()

def load_csv(filepath: str):
    csvHandler.loadConvTable(filepath)

def test_bad_csv_path(): # Tests if the csv given doesn't exist
    with pytest.raises(FileNotFoundError):
        load_csv('sickoMode')