import os
from logparser.query_summary import QuerySummary


def test_parser_method():

    LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'test_data', 'test_log.txt')

    # Initialize the QuerySummary
    qs = QuerySummary()

    # Parse the log file
    result = qs.parser(LOG_FILE_PATH)
    
    # Assertions
    # This is a placeholder. Replace with your actual checks.
    assert isinstance(result, dict)  # if you expect a dictionary, for example
    assert 'some_expected_key' in result  # Replace with actual checks based on the expected output
    
    assert 1