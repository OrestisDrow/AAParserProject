"""
Tests for the `LogFileParser` class from the `logparser` package.

This test module ensures the correct parsing and error handling of the `LogFileParser` class 
when dealing with different log file structures, specifically concerning:
- Valid log files where all expected headers and content lines are present and correctly structured.
- Semi-valid log files where one or more expected headers are missing, and/or some content lines are corrupted.
- Invalid log files where none of the expected headers are found.

The test scenarios include:
- `test_parse_with_valid_log`: Tests the parser's behavior with a completely valid log file.
  It ensures the correct metrics are parsed without any errors being reported.
  
- `test_parse_with_semivalid_log`: Evaluates the parser's behavior with a semi-valid log file.
  It confirms the parser can detect missing headers and corrupted lines, raise appropriate warnings, 
  and still correctly parse valid sections of the log.

- `test_parse_with_invalid_log`: Assesses how the parser behaves with an invalid log file, where
  none of the expected headers are found. It ensures the parser raises an appropriate error and doesn't 
  produce any parsed data.

Usage:
    This module can be run directly or imported as part of a larger test suite.

Example:
    $ pytest test_log_file_parser.py

Notes:
    To broaden the coverage of the tests, consider adding variations in log structures or 
    creating new scenarios that test edge cases or unique log file structures. These test scenarios that
    I have should probably cover most "common" cases.

    As you may observe, tests for the LogFileParser class only include its .parse() methhod and not
    the ._extract_headers() and ._extract_lines(). The reason behind this decision is because I want
    to focus more on Bheaviour, followed by Public Interface, Encapsulation, Refactoring Flexibility.
    and Efficiency. My logic in this case is that since these other private methods are encapsulated in 
    the .parse() method this test will be more of an E2E test than a unit test.   
"""
import pytest
from logparser.log_file_parser import LogFileParser

# Paths to your test logs.
PATH_TO_VALID_LOG = "tests/test_data/test_log_valid.txt"
PATH_TO_INVALID_LOG = "tests/test_data/test_log_invalid.txt"
PATH_TO_SEMIVALID_LOG = "tests/test_data/test_log_semivalid.txt"


@pytest.fixture(params=[PATH_TO_VALID_LOG, PATH_TO_INVALID_LOG, PATH_TO_SEMIVALID_LOG])
def setup_log_file_parser(request):
    parser = LogFileParser(request.param)
    return parser, request.param


def test_parse_with_valid_log(setup_log_file_parser):

    # Case when all headers are there, no corrupt lines
    parser, log_file_path = setup_log_file_parser
    
    if log_file_path != PATH_TO_VALID_LOG:
        pytest.skip("This combination makes no sense for testing so skip.")
    
    parser.parse()
    query_summary, query_errors = parser.query_summary, parser.query_errors
    task_summary, task_errors = parser.task_summary, parser.task_errors
    detailed_summary, detailed_errors = parser.detailed_summary, parser.detailed_errors

    assert query_summary, query_errors == {{'Compile Query': '7.43',
                            'Get Query Coordinator (AM)': '0.00',
                            'Prepare Plan': '8.69',
                            'Run DAG': '80.54',
                            'Start DAG': '1.45',
                            'Submit Plan': '0.48'},
                            []}
    assert task_summary, task_errors == {{'Map 1': {'DURATION': 65013.0, 'CPU_TIME': 516890.0, 'GC_TIME': 7624.0, 'INPUT_RECORDS': 13119189.0, 'OUTPUT_RECORDS': 1200.0}, 
                            'Map 3': {'DURATION': 6061.0, 'CPU_TIME': 66320.0, 'GC_TIME': 1237.0, 'INPUT_RECORDS': 2058.0, 'OUTPUT_RECORDS': 31.0}, 
                            'Map 4': {'DURATION': 7088.0, 'CPU_TIME': 50530.0, 'GC_TIME': 1117.0, 'INPUT_RECORDS': 431.0, 'OUTPUT_RECORDS': 431.0}, 
                            'Reducer 2': {'DURATION': 40112.0, 'CPU_TIME': 110070.0, 'GC_TIME': 1460.0, 'INPUT_RECORDS': 1200.0, 'OUTPUT_RECORDS': 0.0}, 
                            'Reducer 34': {'DURATION': 40112.0, 'CPU_TIME': 110070.0, 'GC_TIME': 1460.0, 'INPUT_RECORDS': 1200.0, 'OUTPUT_RECORDS': 0.0}},
                            []}

    assert detailed_summary, detailed_errors == {{'org.apache.tez.common.counters.DAGCounter': {'NUM_SUCCEEDED_TASKS': 58.0, 'TOTAL_LAUNCHED_TASKS': 58.0, 'DATA_LOCAL_TASKS': 26.0, 'RACK_LOCAL_TASKS': 6.0, 'AM_CPU_MILLISECONDS': 43650.0, 'AM_GC_TIME_MILLIS': 422.0}, 
                                'File System Counters': {'FILE_BYTES_READ': 954341.0, 'FILE_BYTES_WRITTEN': 207491.0, 'HDFS_BYTES_READ': 225077992.0, 'HDFS_BYTES_WRITTEN': 120034.0, 'HDFS_READ_OPS': 44090.0, 'HDFS_WRITE_OPS': 52.0, 'HDFS_OP_CREATE': 26.0, 'HDFS_OP_GET_FILE_STATUS': 78.0, 'HDFS_OP_OPEN': 44012.0, 'HDFS_OP_RENAME': 26.0}, 
                                'File System Whatever': {'ORESTIS_CUSTOM_CORRECT_METRIC': 26.0}},
                            []}
    

def test_parse_with_semivalid_log(setup_log_file_parser):

    # Case where some headers are missing but at least 1 header exists, some lines can have errors -> Semi Valid Log
    parser, log_file_path = setup_log_file_parser
    
    if log_file_path != PATH_TO_SEMIVALID_LOG:
        pytest.skip("This combination makes no sense for testing so skip")
    
    # Expect a UserWarning about missing headers
    with pytest.warns(UserWarning, match="Headers not found: INFO  : Task Execution Summary, INFO  : org.apache.tez.common.counters.DAGCounter:. Headers found: INFO  : Query Execution Summary."):
        parser.parse()

    query_summary, query_errors = parser.query_summary, parser.query_errors
    task_summary, task_errors = parser.task_summary, parser.task_errors
    detailed_summary, detailed_errors = parser.detailed_summary, parser.detailed_errors

    assert query_summary == {'Compile Query': '7.43',
                            'Get Query Coordinator (AM)': '0.00',
                            'Prepare Plan': '8.69',
                            'Run DAG': '80.54',
                            'Start DAG': '1.45',
                            'Submit Plan': '0.48'}
    assert query_errors == ["Err parsing idx: 18, line: 'INFO  : Some Operation                         123.45dsad'. Line has corrupt structure... skipped"]
    assert task_summary is None, task_errors is None
    assert detailed_summary is None, detailed_errors is None


def test_parse_with_invalid_log(setup_log_file_parser):
    # An invalid log would be the case where there are no headers in the logfile found
    parser, log_file_path = setup_log_file_parser
    
    if log_file_path != PATH_TO_INVALID_LOG:
        pytest.skip("This combination makes no sense for testing so skip.")
    
    with pytest.raises(ValueError, match="No headers found in the log file."):
        parser.parse()
    
    # The other values after the expected error should be all None in this case:
    query_summary, query_errors = parser.query_summary, parser.query_errors
    task_summary, task_errors = parser.task_summary, parser.task_errors
    detailed_summary, detailed_errors = parser.detailed_summary, parser.detailed_errors

    assert query_summary is None, query_errors is None
    assert task_summary is None, task_errors is None
    assert detailed_summary is None, detailed_errors is None
    
