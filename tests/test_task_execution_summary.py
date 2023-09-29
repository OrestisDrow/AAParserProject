"""
Tests for the `TaskExecutionSummary` class from the `logparser` package.

This test module focuses on ensuring that the `TaskExecutionSummary` class correctly
parses provided log lines related to task execution into a structured format. 
It aims to verify that durations, CPU times, GC times, input records, and output records are accurately captured. 
Furthermore, the tests check if errors in the log lines, such as corrupt lines or incorrect formats, 
are correctly identified and reported.

Tests include:
- `test_parse_correct_lines`: Validates that given structurally correct log lines, 
  the parser can correctly parse them into the desired format without reporting any errors.
  
- `test_parse_incorrect_lines`: Checks the parser's ability to detect lines with 
  corrupt structures or incorrect formats and subsequently report them.

Usage:
    This module can be run directly or imported as part of a larger test suite.

Example:
    $ pytest test_task_execution_summary.py

Notes:
    To enhance the tests, consider adding edge cases or variations in log structures 
    to ensure the parser handles all possible scenarios comprehensively. These test scenarios that I have should
    probably cover most "common" cases.

    Even though the _parse method is private and testing private methods is an anti-pattern, in
    our case it is important for Granularity, Isolation and Correctness purposes
"""

import re
from logparser.task_execution_summary import TaskExecutionSummary

def test_parse_correct_lines():
    # This test will check if the parse method can correctly parse valid log lines for task execution summary
    sample_lines = [
        (0, "INFO  :      Map 1          65013.00        516,890          7,624      13,119,189            1,200"),
        (1, "INFO  :  Reducer 34          40112.00        110,070          1,460           1,200                0"),
    ]
    
    ts = TaskExecutionSummary(sample_lines)
    assert ts.data == ({'Map 1': {'DURATION': 65013.0, 'CPU_TIME': 516890, 'GC_TIME': 7624, 'INPUT_RECORDS': 13119189, 'OUTPUT_RECORDS': 1200}, 
                        'Reducer 34': {'DURATION': 40112.00, 'CPU_TIME': 110070, 'GC_TIME': 1460, 'INPUT_RECORDS': 1200, 'OUTPUT_RECORDS': 0}},
                        [])

def test_parse_incorrect_lines():
    # This test will check if the parse method correctly identifies and reports errors for invalid lines 
    sample_lines = [
        (0, "INFO  :      Map 1          65013.00        516,890          7,624      13,119,189            1,200"),
        (1, "INFO  :  Reducer 34          40112.00        110,070          1,460           1,200                0"),
        (2, "COMPLETELY INCORRECT LINE sadfds fsadfasdfaf gghvklvc.,/jhjl;;ljkjkh;l"),
        (3, "INFO  :  Map 4          40112.00s        110,070          1,460           1,200                0"), # Notice the "s", this line is corrupt
        (4, "INFO  :  Reducer 123          40112.00        110,070          1,460           1,200                0"),
        (5, "hello world"),
    ]

    ts = TaskExecutionSummary(sample_lines)
    assert ts.data == ({'Map 1': {'DURATION': 65013.0, 'CPU_TIME': 516890, 'GC_TIME': 7624, 'INPUT_RECORDS': 13119189, 'OUTPUT_RECORDS': 1200}, 
                         'Reducer 34': {'DURATION': 40112.0, 'CPU_TIME': 110070, 'GC_TIME': 1460, 'INPUT_RECORDS': 1200, 'OUTPUT_RECORDS': 0}, 
                         'Reducer 123': {'DURATION': 40112.0, 'CPU_TIME': 110070, 'GC_TIME': 1460, 'INPUT_RECORDS': 1200, 'OUTPUT_RECORDS': 0}},
                        ["Err parsing idx: 2, line: 'COMPLETELY INCORRECT LINE sadfds fsadfasdfaf gghvklvc./jhjl;;ljkjkh;l'. Line has corrupt structure... skipped",
                         "Err parsing idx: 3, line: 'INFO  :  Map 4          40112.00s        110070          1460           1200                0'. Line has corrupt structure... skipped",
                         "Err parsing idx: 5, line: 'hello world'. Line has corrupt structure... skipped"])

