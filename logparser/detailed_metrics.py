import re

class DetailedMetrics:
    """
    DetailedMetrics class is purposed to parse and extract detailed metrics from the given log data.

    Attributes:
        _data (tuple): A tuple containing parsed detailed metrics and errors encountered during parsing.

    Methods:
        __init__(self, lines): Constructor that initializes the DetailedMetrics object and initiates the parsing process.
        data: A property that returns the parsed detailed metrics.
        _parse(self, lines): A private method that performs the actual parsing of provided log lines.

    Description:
        The class primarily targets the extraction of specific metrics situated under various headers in the log data. 
        Each header designates a category or context for the metrics that follow it, and the metrics themselves comprise 
        of a name and a value.

        The class employs regular expressions to discern between headers and metric lines. Once a header line is identified, 
        subsequent metric lines are grouped under it until a new header is encountered.

    Usage:
        Instantiate the class with a list of log lines intended for parsing:
            detailed_metrics = DetailedMetrics(lines)
        Access the parsed data using the 'data' property:
            data, errors = detailed_metrics.data

    Notes:
        Headers are lines that specify a category for the subsequent metrics. If a line fails to match the pattern of 
        either a header or a metric, it is flagged as an error.
    """
    def __init__(self, lines):
        """Constructor that initializes the DetailedMetrics object and initiates the parsing process."""
        self._data = self._parse(lines)
    
    @property
    def data(self):
        """Returns the parsed detailed metrics."""
        return self._data

    def _parse(self, lines):
        """Parses the provided log lines to extract and categorize detailed metrics."""
        # Regexes to identify if a line is a header or a metric
        header_pattern = re.compile(r"^INFO\s{2}:\s([\w\s\.]+):$")
        metric_pattern = re.compile(r"^INFO\s{2}:\s{4}([\w_]+):\s(\d+.\d*|\d*)$")


        data = {}
        current_header = None
        errors = []
        
        for idx, line in lines:
            if header_pattern.search(line):
                split_line = line.split("INFO  : ")
                if len(split_line) < 2:
                    errors.append(f"Unexpected header format at idx: {idx}, line: '{line}'.")
                    continue
                current_header = split_line[1].split(":")[0].strip()
                data[current_header] = {}
            elif metric_pattern.search(line) and current_header:
                match = metric_pattern.search(line)
                metric_name = match.group(1)
                metric_value = float(match.group(2))
                data[current_header][metric_name] = metric_value
            else:
                errors.append(f"Err parsing idx: {idx}, line: '{line}'. Corrupt line, failed to match either header or metric pattern... skipped")
                continue
            
        return data, errors