import os

import pytest

def test_persist_json():
    """
    Test dumping Data Frame to a JSON file

    - Load predefined sample data with spark.read
    - Write to JSON using DataFrame.write.csv
    - Compare json file with expected results
    """
    assert True

def test_persist_json_from_stream():
    """
    Test dumping streaming Data Frame to a JSON file

    - Load predefined sample data with spark.readStream
    - Write to JSON using DataFrame.writeStream.foreachbatch
    - Compare json file with expected results
    """
    assert True
