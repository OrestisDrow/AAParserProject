import re

class TaskExecutionSummary:
    """
    TaskExecutionSummary class is designed to parse specific lines of log data to extract summaries of task executions.

    Attributes:
        _data (tuple): A tuple containing parsed task execution summary data and errors encountered during parsing.

    Methods:
        __init__(self, lines): Constructor that initializes the TaskExecutionSummary object and initiates the parsing process.
        data: A property that returns the parsed task execution summary data.
        _parse(self, lines): A private method that performs the actual parsing of provided log lines.

    Description:
        The primary purpose of the class is to identify and extract detailed metrics about task executions from the 
        provided log lines. These metrics include operation durations, CPU times, garbage collection times, input records, 
        and output records. The class uses regular expressions to parse these metrics from each valid log line.

        Each parsed line is expected to contain a specific task identifier (referred to as 'vertice' in the code) followed 
        by the metrics values. The values are then stored in a dictionary with the 'vertice' as the key.

    Usage:
        Instantiate the class with a list of log lines meant for parsing:
            task_execution_summary = TaskExecutionSummary(lines)
        Access the parsed data using the 'data' property:
            data, errors = task_execution_summary.data

    Notes:
        If a log line doesn't fit the expected format, it's deemed an error and is reported while also being skipped from summary.
        Commas within the log lines are removed to ensure accurate numeric conversion of metric values.
    """
    def __init__(self, lines):
        """Constructor that initializes the TaskExecutionSummary object and initiates the parsing process."""
        self._data = self._parse(lines)
    
    @property
    def data(self):
        """Returns the parsed task execution summary data."""
        return self._data
    
    def _parse(self, lines):
        """Parses the provided log lines to extract summaries of task executions."""
        metrics = [
            "DURATION(ms)",
            "CPU_TIME(ms)",
            "GC_TIME(ms)",
            "INPUT_RECORDS",
            "OUTPUT_RECORDS"
        ]
        summary = {}
        errors = []

        # Make a regex of what a correct line pattern will look like for Task Summary lines
        pattern = re.compile(r"^INFO\s{2}:\s+([a-zA-Z]+)\s(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)")

        for idx, line in lines:
            # Remove commas from the line
            line = line.replace(",", "")

            match = pattern.search(line)
            if match:
                vertice = f"{match.group(1)} {match.group(2)}"
                metrics = {
                    "DURATION": float(match.group(3)),
                    "CPU_TIME": float(match.group(4)),
                    "GC_TIME": float(match.group(5)),
                    "INPUT_RECORDS": float(match.group(6)),
                    "OUTPUT_RECORDS": float(match.group(7))
                }
                summary[vertice] = metrics
            else:
                errors.append(f"Err parsing idx: {idx}, line: '{line}'. Line has corrupt structure... skipped")
                continue

        return summary, errors

