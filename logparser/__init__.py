"""
logparser package

This package provides utilities for parsing specific structured details and metrics from a log file. 

Modules:
- `QuerySummary`: Provides functionality to parse and extract summary metrics related to query execution.
- `TaskExecutionSummary`: Used for parsing and summarizing metrics related to task executions in the log.
- `DetailedMetrics`: Captures more granular metrics and details from the log, organizing them under relevant headers.
- `LogFileParser`: Acts as a comprehensive parser that coordinates the parsing of all sections of the log, handling errors, and organizing results.

This `__init__.py` file makes the classes from these modules directly accessible under the `logparser` namespace for convenience.

Example:
    from logparser import LogFileParser

Note:
    To extend the capabilities of this package, new modules can be added, and their primary classes or functions should be imported here for better accessibility.
"""
from logparser.query_summary import QuerySummary
from logparser.task_execution_summary import TaskExecutionSummary
from logparser.detailed_metrics import DetailedMetrics
from logparser.log_file_parser import LogFileParser

