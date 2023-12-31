import warnings
import os 
from .detailed_metrics import DetailedMetrics
from .query_summary import QuerySummary 
from .task_execution_summary import TaskExecutionSummary

class LogFileParser:
    """
    LogFileParser is a class designed to extract and structure key metrics and errors from a specified log file.

    Attributes:
        query_summary (dict): Parsed summary data of the query execution.
        query_errors (list): List of errors encountered while parsing the query execution.
        task_summary (dict): Parsed summary data of task execution.
        task_errors (list): List of errors encountered while parsing the task execution.
        detailed_summary (dict): Parsed detailed metrics.
        detailed_errors (list): List of errors encountered while parsing detailed metrics.
        _header_idxs (dict): Dictionary containing key headers and their corresponding line indexes within the log file.
        _lines (list): List of all lines in the log file, each entry is a tuple of the line's index and content.

    Methods:
        __init__(self, log_file_path): Constructor that initializes the LogFileParser object and reads the log file.
        _extract_headers(self): Identifies and saves the line indexes of key headers within the log file.
        _extract_lines(self): Extracts the lines of interest between the identified headers.
        parse(self): Calls helper methods to extract and parse the log data into structured summaries.
        save(self): Saves the parsed summaries and parser logs (errors) to specified directory paths.
        delete(self): Deletes the previously saved summaries and parser logs.

    Description:
        This class serves as a comprehensive utility to parse a log file. It identifies sections of the log file based on headers, 
        extracts the relevant lines within these sections, and then leverages specialized parser classes (like DetailedMetrics,
        QuerySummary, and TaskExecutionSummary) to structure this data. Furthermore, it has capabilities to save the parsed 
        results and logs to disk and to remove these saved files.

    Notes:
        The parsing process relies heavily on the structure of the log file, making use of specific headers to delineate 
        sections of interest. Any structural inconsistencies or deviations from the expected format may lead to parsing 
        errors, which are saved and can be reviewed.
    """
    def __init__(self, log_file_path):
        """Constructor that initializes the LogFileParser object and reads the log file."""
        self.query_summary = None
        self.query_errors = None
        self.task_summary = None
        self.task_errors = None
        self.detailed_summary = None
        self.detailed_errors = None
        self._header_idxs = {
            "INFO  : Query Execution Summary": None,
            "INFO  : Task Execution Summary": None,
            "INFO  : org.apache.tez.common.counters.DAGCounter:": None,
            }
        
        with open(log_file_path, 'r') as file:
            self._lines = [[index+1, line] for index, line in enumerate(file.read().splitlines())]
        
    def _extract_headers(self):
        """Identifies and saves the line indexes of key headers within the log file."""
        for indx, line in self._lines:
            if line not in list(self._header_idxs.keys()):
                continue
            # We only keep the indexes of the first encounter with each header in the logfile, if multiple same headers are found, give warning and ignore appearences after the first
            if self._header_idxs[line] is None:
                self._header_idxs[line] = indx
            else:
                warnings.warn(f"Header: {line} | found multiple times in the log file... ignoring all but the first instance ...", stacklevel=2)

        # Throw warning and ignore missing headers, if no headers are found at all, throw error
        not_found_headers = [header for header, idx in self._header_idxs.items() if idx is None]

        if len(not_found_headers) == len(self._header_idxs):
            raise ValueError("No headers found in the log file.")
        elif not_found_headers:
            found_headers = [header for header, idx in self._header_idxs.items() if idx is not None]
            warnings.warn(f"Headers not found: {', '.join(not_found_headers)}. Headers found: {', '.join(found_headers)}.", stacklevel=2)
        # This is a command method, return none 

    def _extract_lines(self):
        """Extracts the lines of interest between the identified headers."""
        # Ensure the headers have been extracted
        if not any(self._header_idxs.values()):
            self._extract_headers()

        query_execution_start, query_execution_identifier = self._header_idxs["INFO  : Query Execution Summary"], "INFO  : -------"
        task_execution_start, task_execution_identifier = self._header_idxs["INFO  : Task Execution Summary"], "INFO  : -------"
        detailed_metrics_start, detailed_metrics_identifier = self._header_idxs["INFO  : org.apache.tez.common.counters.DAGCounter:"], "INFO  : Completed executing command(queryId="
        
        def extract_lines_until_identifier(start_idx, finish_identifier):
            # Case where header was not found in the first place
            if start_idx is None:
                return None
            
            idx = start_idx
            while idx < len(self._lines) and finish_identifier not in self._lines[idx][1]:
                idx += 1
            return self._lines[start_idx:idx]
        
        # Some index adjustments are needed for the starting index because the actual lines that we are interested in dont start from header while also they differ between Query/Task and Detailed
        # If any structural errors further exist in the logfile, the other classes which are more specific to each metric type will throw it
        query_execution_lines = extract_lines_until_identifier(query_execution_start+3, query_execution_identifier) if query_execution_start is not None else None
        task_execution_lines = extract_lines_until_identifier(task_execution_start+3, task_execution_identifier) if task_execution_start is not None else None
        detailed_metrics_lines = extract_lines_until_identifier(detailed_metrics_start-1, detailed_metrics_identifier) if detailed_metrics_start is not None else None
        
        return query_execution_lines, task_execution_lines, detailed_metrics_lines 
    
    def parse(self):
        """Calls helper methods to extract and parse the log data into structured summaries."""
        self._extract_headers()
        query_execution_lines, task_execution_lines, detailed_metrics_lines = self._extract_lines()

        self.query_summary, self.query_errors = QuerySummary(query_execution_lines).data if query_execution_lines else (None, None)
        self.task_summary, self.task_errors = TaskExecutionSummary(task_execution_lines).data if task_execution_lines else (None, None)
        self.detailed_summary, self.detailed_errors = DetailedMetrics(detailed_metrics_lines).data if detailed_metrics_lines else (None, None)        

    def save(self):
        """Saves the parsed summaries and parser logs (errors) to specified directory paths."""
        # Ensure directories exist
        if not os.path.exists('./RunResults/Summaries/'):
            os.makedirs('./RunResults/Summaries/')
        if not os.path.exists('./RunResults/ParserLogs/'):
            os.makedirs('./RunResults/ParserLogs/')
        
        # Remove existing summaries
        summaries = ['query_summary.txt', 'task_summary.txt', 'detailed_summary.txt']
        for summary_file in summaries:
            summary_path = os.path.join('./RunResults/Summaries/', summary_file)
            if os.path.exists(summary_path):
                os.remove(summary_path)
        
        # Remove existing parser_error_logs.txt
        if os.path.exists('./RunResults/ParserLogs/parser_error_logs.txt'):
            os.remove('./RunResults/ParserLogs/parser_error_logs.txt')
        
        # Write the summaries
        with open('./RunResults/Summaries/query_summary.txt', 'w') as f:
            f.write(str(self.query_summary))
        with open('./RunResults/Summaries/task_summary.txt', 'w') as f:
            f.write(str(self.task_summary))
        with open('./RunResults/Summaries/detailed_summary.txt', 'w') as f:
            f.write(str(self.detailed_summary))
        
        # Write the errors
        with open('./RunResults/ParserLogs/parser_error_logs.txt', 'w') as f:
            f.write("===============================\n")
            f.write("Query Summary Errors:\n")
            f.write("===============================\n")
            for error in self.query_errors or []:
                f.write(error + "\n")
            f.write("\n===============================\n")
            f.write("Task Execution Errors:\n")
            f.write("===============================\n")
            for error in self.task_errors or []:
                f.write(error + "\n")
            f.write("\n===============================\n")
            f.write("Detailed Metrics Errors:\n")
            f.write("===============================\n")
            for error in self.detailed_errors or []:
                f.write(error + "\n")

    def delete(self):
        """Deletes the previously saved summaries and parser logs."""
        # List of summary files to delete
        summaries = ['query_summary.txt', 'task_summary.txt', 'detailed_summary.txt']
        
        # Remove summary files
        for summary_file in summaries:
            summary_path = os.path.join('./RunResults/Summaries/', summary_file)
            if os.path.exists(summary_path):
                os.remove(summary_path)
        
        # Remove parser_error_logs.txt
        if os.path.exists('./RunResults/ParserLogs/parser_error_logs.txt'):
            os.remove('./RunResults/ParserLogs/parser_error_logs.txt')
