import os
from logparser.log_file_parser import LogFileParser

def main():
    # Assume the log file is in the root directory of your package
    log_file_path = os.path.join(os.path.dirname(__file__), "logfile.txt")

    parser = LogFileParser(log_file_path)

    # Using the parse() method
    parsed_data = parser.parse()

    # Using the save() method to save results to a file
    # Saving to the current directory for simplicity
    parser.save(".")

if __name__ == "__main__":
    main()
