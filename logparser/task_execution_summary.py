import re

class TaskExecutionSummary:
    def __init__(self, lines):
        self._data = self._parse(lines)
    
    @property
    def data(self):
        return self._data
    
    def _parse(self, lines):
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

