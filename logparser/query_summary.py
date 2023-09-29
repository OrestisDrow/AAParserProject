import re

class QuerySummary:
    """
    QuerySummary class is responsible for parsing specific lines of log data to extract the summaries of query operations.

    Attributes:
        _data (tuple): A tuple containing parsed summary data and errors encountered during parsing.

    Methods:
        __init__(self, lines): Constructor that initializes the QuerySummary object and triggers the parsing process.
        data: A property that returns the parsed data.
        _parse(self, lines): A private method that performs the actual parsing of provided log lines.

    Description:
        The class is designed to identify and extract information about critical query operations and their respective
        execution durations from the provided log lines. The critical operations are predefined and consist of operations
        such as "Compile Query", "Prepare Plan", etc. The class uses regular expressions to identify valid log lines, extract 
        the operation names and their durations, and finally returns the parsed data and any errors encountered during the 
        parsing process.

    Usage:
        Instantiate the class with a list of log lines to be parsed:
            query_summary = QuerySummary(lines)
        Access the parsed data using the 'data' property:
            data, errors = query_summary.data

    Notes:
        If a log line doesn't match the expected structure, it's considered as an error and is reported while it is also skipped from the summary.
        If any of the critical operations are missing from the log lines, an error is reported for each missing operation.
    """

    def __init__(self, lines):
        """Constructor that initializes the QuerySummary object and triggers the parsing process."""
        self._data = self._parse(lines)
    
    @property
    def data(self):
        """Returns the parsed data."""
        return self._data
    
    def _parse(self, lines):
        """Parses the provided log lines to extract the summaries of query operations."""
        critical_operations = [
            "Compile Query",
            "Prepare Plan",
            "Get Query Coordinator (AM)",
            "Submit Plan",
            "Start DAG",
            "Run DAG"
        ]
        summary = {}
        errors = []

        encountered_operations = set()

        # Make a regex of what a correct line pattern will look like for Query Summary lines
        pattern = re.compile(r"^INFO\s{2}:\s([a-zA-Z()]+(?:\s[a-zA-Z()]+)*?)\s+([\d.]+)s")

        for idx, line in lines:
            match = pattern.search(line)
            if match:
                operation = match.group(1).rstrip()
                duration = float(match.group(2))
                summary[operation] = f'{duration:.2f}'
                encountered_operations.add(operation)
            else:
                errors.append(f"Err parsing idx: {idx}, line: '{line.rstrip()}'. Line has corrupt structure... skipped")
                continue

        # If any critical operation is missing, append to the err
        for op in critical_operations:
            if op not in encountered_operations:
                errors.append(f"Critical operation: '{op}' missing in the log data.")

        return summary, errors



