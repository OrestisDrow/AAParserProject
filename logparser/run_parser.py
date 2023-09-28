import os
from logparser.log_file_parser import LogFileParser

def main():
    # Assume the log file is in the root directory of your package with the name logfile.txt
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logfile.txt")
    log_file_path = os.path.normpath(log_file_path)  # Normalize the path to resolve any '..' segments


    parser = LogFileParser(log_file_path)

    # Using the parse() method
    parsed_data = parser.parse()

    # Using the save() method to save results to a file
    # Saving to the current directory for simplicity
    parser.save(".")

if __name__ == "__main__":
    main()
