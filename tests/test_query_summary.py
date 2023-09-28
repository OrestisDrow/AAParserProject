import re
from logparser.query_summary import QuerySummary

def test_parse_correct_lines():
    # This test will check if the parse method can correctly parse valid log lines for query summary
    # Note that these lines are structurally correct while also all the 6 critical operations are there, this is why expected error should be empty
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

