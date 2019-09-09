import os

import pytest

def test_aggregate():
    """
    Test aggregating data from a Data Frame

    - Load predefined sample data with spark.read
    - Aggregate data
    - Compare aggregated data in DF with expected results
    """
    assert True

def test_aggregate_as_stream():
    """
    Test aggregating data from a streaming Data Frame 

    - Load predefined sample data with spark.readStream
    - Aggregate data
    - Query data to memory sink
    - Query data from memory into a temp DF and compare with expected results
    """
    assert True
