""" 
LogParser Package

This package provides functionality to parse specific log files 
and extract relevant data for analysis.

Classes:
- LogFileParser: Main class to initiate the log parsing.
- QuerySummary: Extracts summary and errors of the query execution lines.
- TaskExecutionSummary: Extracts summary and errors of task execution lines.
- DetailedMetrics: Extracts detailed metrics and errors from detailed metrics lines.
"""
from logparser.query_summary import QuerySummary
from logparser.task_execution_summary import TaskExecutionSummary
from logparser.detailed_metrics import DetailedMetrics
from logparser.log_file_parser import LogFileParser

