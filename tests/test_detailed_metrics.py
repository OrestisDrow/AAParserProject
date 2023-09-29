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
