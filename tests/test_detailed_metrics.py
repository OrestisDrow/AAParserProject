"""
Tests for the `DetailedMetrics` class from the `logparser` package.

This test module focuses on ensuring that the `DetailedMetrics` class correctly
parses provided log lines related to detailed performance metrics into a structured format. 
It aims to verify that metrics are accurately captured and organized.

The test scenarios include:
- `test_parse_correct_lines`: Validates that given structurally correct log lines, 
  the parser can correctly parse them into the desired format without reporting any errors. 
  
- `test_parse_incorrect_lines`: Assesses the parser's capability to detect lines with 
  corrupt structures or incorrect formats and subsequently report them.

Usage:
    This module can be run directly or imported as part of a larger test suite.

Example:
    $ pytest test_detailed_metrics.py

Notes:
    To enhance the tests, consider adding edge cases or variations in log structures 
    to ensure the parser handles all possible scenarios comprehensively. These test scenarios that
    I have should probably cover most "common" cases.

    Even though the _parse method is private and testing private methods is an anti-pattern, in
    our case it is important for Granularity, Isolation and Correctness purposes
"""

import re
from logparser.detailed_metrics import DetailedMetrics

def test_parse_correct_lines():
    # This test will check if the parse method can correctly parse valid lines for detailed metrics
    sample_lines = [
        (0, "INFO  : org.apache.tez.common.counters.DAGCounter:"),
        (1, "INFO  :    NUM_SUCCEEDED_TASKS: 58"),
        (2, "INFO  :    TOTAL_LAUNCHED_TASKS: 58"),
        (3, "INFO  :    DATA_LOCAL_TASKS: 26"),
        (4, "INFO  : File System Counters:"),
        (5, "INFO  :    FILE_BYTES_READ: 954341"),
        (6, "INFO  :    FILE_BYTES_WRITTEN: 207491"),
        (7, "INFO  :    HDFS_BYTES_READ: 225077992"),
        (8, "INFO  :    HDFS_BYTES_WRITTEN: 120034"),
        (9, "INFO  :    HDFS_READ_OPS: 44090"),
    ]
    
    dm = DetailedMetrics(sample_lines)
    assert dm.data == ({'org.apache.tez.common.counters.DAGCounter': {'NUM_SUCCEEDED_TASKS': 58.0,
                                                                        'TOTAL_LAUNCHED_TASKS': 58.0,
                                                                            'DATA_LOCAL_TASKS': 26.0},
                         'File System Counters': {'FILE_BYTES_READ': 954341.0,
                                                   'FILE_BYTES_WRITTEN': 207491.0,
                                                     'HDFS_BYTES_READ': 225077992.0,
                                                       'HDFS_BYTES_WRITTEN': 120034.0,
                                                         'HDFS_READ_OPS': 44090.0}},
                        [])

def test_parse_incorrect_lines():
    # This test will check if the parse method correctly identifies and reports errors for invalid lines 
    sample_lines = [
        (0, "INFO  : org.apache.tez.common.counters.DAGCounter:"),
        (1, "INFO  :    NUM_SUCCEEDED_TASKS: 58"),                      
        (2, "INFO  :    TOTAL_LAUNCHED_TASKS: 58 sdafasfsa dfgfh;;"),   # Corrupt
        (3, "INFO  : File System Counters:"),
        (4, "INFO  :    HDFS_OP_OPEN: 44012asdf"),                      # Corrupt
        (5, "INFO  :    HDFS_OP_RENAME: 26"),
        (6, "INFO  : currUpT lIneE asd gdfghghjkgfdhjhgkfj "),          # Corrupt
        (7, "INFO  :    METRIC_ONE: 26"),                               
        (8, "INFO  :    METRIC_TWO: 26"),                               
    ]
    

    dm = DetailedMetrics(sample_lines)
    assert dm.data == ({'org.apache.tez.common.counters.DAGCounter': {'NUM_SUCCEEDED_TASKS': 58.0}, 
                        'File System Counters': {'HDFS_OP_RENAME': 26, 'METRIC_ONE': 26.0, 'METRIC_TWO': 26.0}},
                        ["Err parsing idx: 2, line: 'INFO  :    TOTAL_LAUNCHED_TASKS: 58 sdafasfsa dfgfh;;'. Corrupt line, failed to match either header or metric pattern... skipped",
                         "Err parsing idx: 4, line: 'INFO  :    HDFS_OP_OPEN: 44012asdf'. Corrupt line, failed to match either header or metric pattern... skipped",
                         "Err parsing idx: 6, line: 'INFO  : currUpT lIneE asd gdfghghjkgfdhjhgkfj '. Corrupt line, failed to match either header or metric pattern... skipped"])
