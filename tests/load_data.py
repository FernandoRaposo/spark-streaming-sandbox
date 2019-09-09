import os

import pytest

def test_load_csv():
    """
    Test loading data from CSV file to a Data Frame using spark.read

    - Load predefined sample data with spark.read
    - Compare to expected Data Frame
    """
    assert True

def test_load_csv_as_stream():

    """
    Test loading data from CSV file to a Data Frame using spark.readStream

    - Load predefined sample data with spark.readStream
    - Write data to memory sink
    - Query data from memory sink into Data Frame
    - Compare to expected Data Frame
    """
    assert True
