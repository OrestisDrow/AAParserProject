import warnings
import os 
from .detailed_metrics import DetailedMetrics
from .query_summary import QuerySummary 
from .task_execution_summary import TaskExecutionSummary

class LogFileParser:
    
    def __init__(self, log_file_path):
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
        for indx, line in self._lines:
            if line not in list(self._header_idxs.keys()):
                continue
            # We only keep the indexes of the first encounter with each header in the logfile, if multiple same headers are found, give warning and ignore appearences after the first
            if self._header_idxs[line] is None:
                self._header_idxs[line] = indx
            else:
                warnings.warn(f"Header: {line} | found multiple times in the log file... ignoring all but the first instance ...", stacklevel=2)

        # Throw warning and ignore missing headers, if no headers are found, throw error
        not_found_headers = [header for header, idx in self._header_idxs.items() if idx is None]

        if len(not_found_headers) == len(self._header_idxs):
            raise ValueError("No headers found in the log file.")
        elif not_found_headers:
            found_headers = [header for header, idx in self._header_idxs.items() if idx is not None]
            warnings.warn(f"Headers not found: {', '.join(not_found_headers)}. Headers found: {', '.join(found_headers)}.", stacklevel=2)
        # This is a command method, return none 

    def _extract_lines(self):
        
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
        
        #pprint(detailed_metrics_lines)
        return query_execution_lines, task_execution_lines, detailed_metrics_lines 
    
    def parse(self):
        self._extract_headers()
        query_execution_lines, task_execution_lines, detailed_metrics_lines = self._extract_lines()

        self.query_summary, self.query_errors = QuerySummary(query_execution_lines).data if query_execution_lines else (None, None)
        self.task_summary, self.task_errors = TaskExecutionSummary(task_execution_lines).data if task_execution_lines else (None, None)
        self.detailed_summary, self.detailed_errors = DetailedMetrics(detailed_metrics_lines).data if detailed_metrics_lines else (None, None)        

    def save(self):
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
        with open('./ParserLogs/parser_error_logs.txt', 'w') as f:
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
