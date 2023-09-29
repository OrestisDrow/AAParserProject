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

