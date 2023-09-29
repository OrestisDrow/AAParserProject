"""
Tests for the `QuerySummary` class from the `logparser` package.

This test module focuses on verifying that the `QuerySummary` class correctly
parses provided log lines into a structured format. It also ensures that errors
in the log lines, such as missing critical operations or lines with corrupt structures, 
are correctly identified and reported.

Tests include:
- `test_parse_correct_lines`: Verifies that given structurally correct log lines with all the 
  expected operations, the parser can correctly parse them into the desired format without 
  reporting any errors.
  
- `test_parse_incorrect_lines`: Validates the parser's ability to detect lines with corrupt structures,
  report them, and also identify any missing critical operations from the logs.

Usage:
    This module can be run directly or imported as part of a larger test suite.

Example:
    $ pytest test_query_summary.py

Notes:
    To extend the tests, consider adding edge cases or variations in log structures to ensure
    the parser handles all possible scenarios. These test scenarios that I have should
    probably cover most "common" cases.

    Even though the _parse method is private and testing private methods is an anti-pattern, in
    our case it is important for Granularity, Isolation and Correctness purposes
"""

import re
from logparser.query_summary import QuerySummary

def test_parse_correct_lines():
    # This test will check if the parse method can correctly parse valid log lines for query summary
    # Note that these lines are structurally correct while also all the 6 critical operations are present
    # This is why expected error should be empty
    sample_lines = [
        (0, "INFO  : Compile Query                           7.43s"),
        (1, "INFO  : Prepare Plan                            8.69s"),
        (2, "INFO  : Get Query Coordinator (AM)              0.00s"),
        (3, "INFO  : Submit Plan                             0.48s"),
        (4, "INFO  : Start DAG                               1.45s"),
        (5, "INFO  : Run DAG                                80.54s"),
    ]
    
    qs = QuerySummary(sample_lines)
    assert qs.data == ({'Compile Query': '7.43',
                         'Prepare Plan': '8.69',
                         'Get Query Coordinator (AM)': '0.00',
                         'Submit Plan' : '0.48',
                         'Start DAG': '1.45',
                         'Run DAG': '80.54',
                        },
                        [])

def test_parse_incorrect_lines():
    # This test will check if the parse method correctly identifies and reports errors for invalid lines
    # Note that in the sample lines, there are 2 comppletely incorrect lines while also a critical operation is missing, 
    # so these 3 cases should showcase that the method can identify both, totally incorrect lines, and, missing critical operations 
    sample_lines = [
        (0, "INFO  : Compile Query                           7.43s"),
        (1, "INFO  : Prepare Plan                            8.69s"),
        (2, "INFO  : Get Query Coordinator (AM)              0.00s"),
        (3, "INFO  : Submit Plan                             0.48s"),
        (4, "INFO  : Start DAG                               1.45s"),
        #(5, "INFO  : Run DAG                                80.54s"),
        (6, "INCORRECT LINE 1"),
        (6, "INFO da sdasf ffffgdhkgj'dlfl''' : INCORRECT LINE 2"),

    ]

    qs = QuerySummary(sample_lines)
    assert qs.data == ({'Compile Query': '7.43',
                         'Prepare Plan': '8.69',
                         'Get Query Coordinator (AM)': '0.00',
                         'Submit Plan' : '0.48',
                         'Start DAG': '1.45',
                        },
                        ["Err parsing idx: 6, line: 'INCORRECT LINE 1'. Line has corrupt structure... skipped",
                          "Err parsing idx: 6, line: 'INFO da sdasf ffffgdhkgj'dlfl''' : INCORRECT LINE 2'. Line has corrupt structure... skipped", 
                          "Critical operation: 'Run DAG' missing in the log data."])

