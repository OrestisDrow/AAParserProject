import re
class DetailedMetrics:
    def __init__(self, lines):
        self._data = self._parse(lines)
    
    @property
    def data(self):
        return self._data

    def _parse(self, lines):
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