import re

class QuerySummary:
    def __init__(self, lines):
        self._data = self._parse(lines)
    
    @property
    def data(self):
        return self._data
    
    def _parse(self, lines):
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

        # Check if any critical operation is missing
        for op in critical_operations:
            if op not in encountered_operations:
                errors.append(f"Critical operation: '{op}' missing in the log data.")

        return summary, errors



